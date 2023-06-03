<script lang="ts">
    import * as idbKeyval from "idb-keyval";
    import { onMount } from "svelte";

    export let domainName: string;

    let statementTemplates = {
        Blank: "",
        "Operation as normal":
            "I hereby declare that as of {currentDate}, I am still in complete control of {domain} and all its associated data. As the owner and administrator of the website, I have not received any subpoenas or warrants for data, nor have I received any gag order limiting me from informing users as such, and I remain committed to protecting the privacy and security of all users of my website. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Canary provider moved":
            "I hereby declare that as of {currentDate}, I am issuing this statement to inform users that we are moving our canary from Purplix.io to another canary service. As the owner and administrator of the website, I affirm that this change is solely related to the canary service provider and does not indicate any compromise of user data or any legal demands received. The new canary service will provide continued transparency and timely updates regarding the status of user privacy and security.",
        "Warrents - No user data compromised":
            "I hereby declare that as of {currentDate}, I have received a warrant for data related to {domain}. However, I can confirm that no user data has been compromised as a result of this warrant. I am diligently protecting the privacy and security of all users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Warrents - User data compromised":
            "I hereby declare that as of {currentDate}, I have received a warrant for data related to {domain}. User data has been compromised as a result of this warrant. I am taking immediate actions to mitigate the impact, investigate the incident, and notify affected users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Subpoenas - No user data compromised":
            "I hereby declare that as of {currentDate}, I have received a subpoena for data related to {domain}. However, I can confirm that no user data has been compromised as a result of this subpoena. I am diligently protecting the privacy and security of all users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Subpoenas - User data compromised":
            "I hereby declare that as of {currentDate}, I have received a subpoena for data related to {domain}. User data has been compromised as a result of this subpoena. I am taking immediate actions to mitigate the impact, investigate the incident, and notify affected users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Raids - No user data compromised":
            "I hereby declare that as of {currentDate}, there has been a raid or seizure of data related to {domain}. However, I can confirm that no user data has been compromised as a result of this raid. I am diligently protecting the privacy and security of all users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Raids - User data compromised":
            "I hereby declare that as of {currentDate}, there has been a raid or seizure of data related to {domain}. User data has been compromised as a result of this raid. I am taking immediate actions to mitigate the impact, investigate the incident, and notify affected users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Trap and trace orders":
            "I hereby declare that as of {currentDate}, I have received trap and trace orders related to {domain}. User communication may have been monitored or intercepted as a result of these orders. I am actively working to address the situation, protect user privacy, and ensure the integrity of the platform. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
        "Blackmail or extortion":
            "I hereby declare that as of {currentDate}, there have been instances of blackmail or extortion targeting {domain} or its administrators. I am taking immediate actions to investigate and mitigate the situation, as well as provide support to affected users. This statement will be reviewed and updated as necessary on or before {nextCanary}.",
    } as Record<string, string>;

    let statement = statementTemplates["Operation as normal"].toString();
    let customTemplate = false;

    onMount(async () => {
        const customTemplates = await idbKeyval.get("customCanaryTemplates");
        if (customTemplates) {
            statementTemplates = {
                ...customTemplates,
                ...statementTemplates,
            };
        }
    });

    function onStatementChange() {
        customTemplate = true;
    }

    let saveModelActive = false;
    let customTemplateLabel = "";

    async function saveCustomTemplate() {
        if (customTemplateLabel) {
            const toSave = {};
            const customTemplates = await idbKeyval.get(
                "customCanaryTemplates"
            );
            if (customTemplates) {
                Object.assign(toSave, customTemplates);
            }

            toSave[customTemplateLabel] = statement;

            statementTemplates = {
                [customTemplateLabel]: statement,
                ...statementTemplates,
            };

            await idbKeyval.set("customCanaryTemplates", toSave);

            customTemplate = false;
            saveModelActive = false;
            customTemplateLabel = "";
        }
    }
</script>

<dialog class="surface-variant" class:active={saveModelActive}>
    <h5>Save custom template</h5>
    <form on:submit|preventDefault={saveCustomTemplate}>
        <div class="field label border">
            <input type="text" bind:value={customTemplateLabel} />
            <label for="title">Template label</label>
        </div>

        <nav class="right-align">
            <button
                type="button"
                class="border"
                on:click={() => (
                    (saveModelActive = false), (customTemplateLabel = "")
                )}>Cancel</button
            >
            <button>Save</button>
        </nav>
    </form>
</dialog>

<article>
    <h3>Publish Canary</h3>

    <form>
        <h6>Next canary</h6>
        <nav class="wrap" style="margin-top: 0;">
            <span class="chip round primary">Tomorrow</span>
            <span class="chip round primary">In a week</span>
            <span class="chip round primary disabled">In a fortnight</span>
            <span class="chip round primary">In a month</span>
            <span class="chip round primary">In a year</span>
        </nav>

        <h6>Statement</h6>
        <div
            class="field textarea border extra"
            style="margin-bottom: 0;margin-top: 0;"
        >
            <textarea bind:value={statement} on:input={onStatementChange} />
        </div>
        <nav class="right-align" style="margin-bottom: 1em;">
            <button type="button">
                <span>Statement templates</span>
                <i>arrow_drop_down</i>
                <menu>
                    {#each Object.entries(statementTemplates) as [title, template]}
                        <a
                            href="#{title}"
                            on:click={() => (statement = template)}>{title}</a
                        >
                    {/each}
                </menu>
            </button>
            {#if customTemplate}
                <button
                    type="button"
                    class="fill"
                    on:click={() => (saveModelActive = true)}
                >
                    <i>save</i>
                    <span>Save custom template</span>
                </button>
            {/if}
        </nav>
    </form>
</article>

<style>
    @media only screen and (max-width: 600px) {
        nav {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>