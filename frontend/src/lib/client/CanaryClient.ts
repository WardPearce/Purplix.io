/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseHttpRequest } from './core/BaseHttpRequest';
import type { OpenAPIConfig } from './core/OpenAPI';
import { FetchHttpRequest } from './core/FetchHttpRequest';

import { AccountService } from './services/AccountService';
import { CanaryService } from './services/CanaryService';
import { DefaultService } from './services/DefaultService';
import { DocumentService } from './services/DocumentService';
import { NotificationsService } from './services/NotificationsService';
import { PrivacyService } from './services/PrivacyService';
import { PushService } from './services/PushService';
import { SessionService } from './services/SessionService';
import { SettingsService } from './services/SettingsService';
import { SubscriptionService } from './services/SubscriptionService';
import { SurveyService } from './services/SurveyService';
import { WarrantService } from './services/WarrantService';
import { WebhookService } from './services/WebhookService';

type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;

export class CanaryClient {

    public readonly account: AccountService;
    public readonly canary: CanaryService;
    public readonly default: DefaultService;
    public readonly document: DocumentService;
    public readonly notifications: NotificationsService;
    public readonly privacy: PrivacyService;
    public readonly push: PushService;
    public readonly session: SessionService;
    public readonly settings: SettingsService;
    public readonly subscription: SubscriptionService;
    public readonly survey: SurveyService;
    public readonly warrant: WarrantService;
    public readonly webhook: WebhookService;

    public readonly request: BaseHttpRequest;

    constructor(config?: Partial<OpenAPIConfig>, HttpRequest: HttpRequestConstructor = FetchHttpRequest) {
        this.request = new HttpRequest({
            BASE: config?.BASE ?? 'https://localhost/api',
            VERSION: config?.VERSION ?? '0.0.1',
            WITH_CREDENTIALS: config?.WITH_CREDENTIALS ?? false,
            CREDENTIALS: config?.CREDENTIALS ?? 'include',
            TOKEN: config?.TOKEN,
            USERNAME: config?.USERNAME,
            PASSWORD: config?.PASSWORD,
            HEADERS: config?.HEADERS,
            ENCODE_PATH: config?.ENCODE_PATH,
        });

        this.account = new AccountService(this.request);
        this.canary = new CanaryService(this.request);
        this.default = new DefaultService(this.request);
        this.document = new DocumentService(this.request);
        this.notifications = new NotificationsService(this.request);
        this.privacy = new PrivacyService(this.request);
        this.push = new PushService(this.request);
        this.session = new SessionService(this.request);
        this.settings = new SettingsService(this.request);
        this.subscription = new SubscriptionService(this.request);
        this.survey = new SurveyService(this.request);
        this.warrant = new WarrantService(this.request);
        this.webhook = new WebhookService(this.request);
    }
}

