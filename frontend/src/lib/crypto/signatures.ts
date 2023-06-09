import sodium from "libsodium-wrappers-sumo";
import { get } from "svelte/store";
import { localSecrets } from "../../stores";
import { base64Decode, base64Encode, utf8Decode, utf8Encode } from "./codecUtils";


export class InvalidSignature extends Error {
    constructor() {
        super();
        this.message = "Invalid signature";
        this.name = "InvalidSignature";
    }
}

export class SignKeypairUndefinedError extends Error {
    constructor() {
        super();
        this.message = "Sign Keypair can not be undefined";
        this.name = "SignKeypairUndefinedError";
    }
}

export enum SignaturePublicKeyLocation {
    localKeypair = "localPublicSignKeypair"
}

export enum SignaturePrivateKeyLocation {
    localKeypair = "localPrivateSignKeypair"
}

export type PublicKey = Uint8Array | SignaturePublicKeyLocation | string;
export type PrivateKey = Uint8Array | SignaturePrivateKeyLocation;

export interface KeyPair {
    publicKey: PublicKey;
    privateKey: PrivateKey;
}

export function generateKeypair(): sodium.KeyPair {
    return sodium.crypto_sign_keypair();
}

export function seedKeypair(seed: Uint8Array): sodium.KeyPair {
    return sodium.crypto_sign_seed_keypair(seed);
}

export function determineKeyLocation(key: PublicKey | PrivateKey): Uint8Array {
    if (key instanceof Uint8Array) {
        return key;
    } else if (key === SignaturePublicKeyLocation.localKeypair || key === SignaturePrivateKeyLocation.localKeypair) {
        const storedSecrets = get(localSecrets);
        const keypairKey = key === SignaturePrivateKeyLocation.localKeypair ? "privateKey" : "publicKey";
        if (typeof storedSecrets === "undefined" || !("rawSignKeypair" in storedSecrets) || !(keypairKey in storedSecrets["rawSignKeypair"])) {
            throw new SignKeypairUndefinedError();
        }
        return base64Decode(storedSecrets.rawSignKeypair[keypairKey]);
    } else {
        return base64Decode(key);
    }
}

export function sign(privateKey: PrivateKey, toSign: string | Uint8Array): string {
    const signature = sodium.crypto_sign(
        toSign instanceof Uint8Array ? toSign : utf8Encode(toSign),
        determineKeyLocation(privateKey),
    );
    return base64Encode(signature);
}

export function signHash(privateKey: PrivateKey, toSign: string | Uint8Array): string {
    const hash = sodium.crypto_generichash(
        sodium.crypto_generichash_BYTES,
        toSign instanceof Uint8Array ? toSign : utf8Encode(toSign)
    );
    return sign(privateKey, hash);
}

export function validateHash(
    publicKey: PublicKey, signedMessage: string,
    unsignedMessage: string | Uint8Array
): void {
    const hash = sodium.crypto_generichash(
        sodium.crypto_generichash_BYTES,
        unsignedMessage instanceof Uint8Array ? unsignedMessage : utf8Encode(unsignedMessage)
    );
    validate(publicKey, signedMessage, hash);
}

export function open(
    publicKey: PublicKey, signedMessage: string, utf8: boolean = false
): string | Uint8Array {
    let signedData: Uint8Array;
    try {
        signedData = sodium.crypto_sign_open(
            base64Decode(signedMessage),
            determineKeyLocation(publicKey)
        );
    } catch {
        throw new InvalidSignature();
    }

    return utf8 ? utf8Decode(signedData) : signedData;
}


export function validate(
    publicKey: PublicKey, signedMessage: string,
    unsignedMessage: string | Uint8Array
): void {
    let signedData = open(publicKey, signedMessage, false);

    let unsignedData: Uint8Array;
    if (typeof unsignedMessage === "string") {
        unsignedData = utf8Encode(unsignedMessage);
    } else {
        unsignedData = unsignedMessage;
    }

    if (sodium.to_hex(signedData) !== sodium.to_hex(unsignedData)) {
        throw new InvalidSignature();
    }
}


export default {
    sign,
    open,
    validate,
    seedKeypair,
    generateKeypair,
    validateHash,
    signHash
};