/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type PublishCanaryWarrantModel = {
    signature: string;
    btc_latest_block: string;
    statement?: string;
    concern: PublishCanaryWarrantModel.concern;
};

export namespace PublishCanaryWarrantModel {

    export enum concern {
        NONE = 'none',
        MILD = 'mild',
        MODERATE = 'moderate',
        SEVERE = 'severe',
    }


}

