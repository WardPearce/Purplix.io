# Development is on pause.
I'm busy working on other projects. Syncpad (formally Purplix) will continue development once I have more free time. Consider the current source code a proof of concept.

# This project is NOT production ready.

&nbsp;

<div align="center">
  <img src="https://i.imgur.com/1pkrLq9.png" width="100px" />
  <h1>Purplix</h1>
  <blockquote>
    Purplix is an open-source collection of tools dedicated to user privacy and creating trust with your audience.
  </blockquote>
</div>

&nbsp;

# About
## What is Purplix Survey?
![Purplix survey preview](https://files.catbox.moe/13yjgb.gif)

Purplix Survey is a free & open-source survey tool that can't read your questions and answers.

With traditional surveys, you are one data breach, one rogue employee, or one government warrant away from all your users' data being exposed. Purplix uses modern encryption techniques to keep your users' data away from any actors.

### How does it work?
#### Questions, Descriptions & Title Encryption

When you create a survey, we encrypt your title, descriptions, and questions with a secret key. This key is then stored encrypted in your keychain. When you share your survey with others using a link, the key is stored in the link for your participants. This ensures that your survey questions can only be read by your participants.

#### Answers Encryption
Every survey has its own unique key pair. The private key is securely stored in your keychain, while the public key is used by users to encrypt their answers. Only you have the means to decrypt the answers once they are submitted. When you share a survey, we include a hash of the public key in the URL to prevent man-in-the-middle attacks.

#### Preventing Spam & Multiple Submissions
Survey creators can opt-in to use VPN blocking, requiring a Purplix account, or IP blocking. IP blocking works by storing a hash of the IP salted with a key not stored by Purplix, minimizing the attack surface of tracking submission locations. These IP hashes are only stored for 7 days or until the survey closes. Users will always be informed when any of these features are enabled.

## What is Purplix Canary?
![Image of canary site](https://i.imgur.com/c3HUe1C.png)
Purplix Canary is a free & open-source warrant canary tool that helps you build trust with your users.

It allows you to inform users cryptographically if your site has been compromised, seized, or raided by anyone.

### How does it work?
#### Site Verification
Purplix uses DNS records to verify the domain the canary is for, giving your users confidence that they are trusting the right people.

#### Canary Signatures
Each domain is associated with a unique key pair. The private key is generated locally and securely stored within the owner's keychain. When a user visits a canary from a specific domain for the first time, their private key is used to sign the public key. This signed version of the public key is then automatically employed for subsequent visits, effectively mitigating man-in-the-middle attacks and ensuring the trustworthiness of canary statements from the respective domain.

#### Files
Canaries can include signed documents to help users further understand a situation.

#### Notifications
Users are automatically notified on the event of a new statement being published.

# Have any questions?
[Join our Matrix space](https://matrix.to/#/#ward:matrix.org)
