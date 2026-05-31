# ECHO

### *Edge Computing & Hardware Orchestration*

Home Assistant integration for remote data extraction, processing, and orchestration for  UC Centers and Field Stations Network (RCER UC). 

![ECHO](images/icon.png)


## Installation via HACS

1. The **ECHO integration** is not part of the HACS Store. To install it, you will need to add it as a *custom repository* by following this guide: [HACS Custom Repositories](https://hacs.xyz/docs/faq/custom_repositories/).
2. Download the integration by entering the repository URL and adding it. Then, go to HACS and install it.
3. Once the installation is complete, **restart** Home Assistant.
4. After restarting, navigate to the **Integrations page** to configure the service.


## Service Configuration

ECHO enables automated data extraction from THIES stations, local processing, cloud backup (SharePoint), and alert/task orchestration.

During setup, you will be prompted to provide the following parameters:

### SharePoint Configuration (Cloud Backup)

1. **sharepoint_client_id**: Application Client ID.
2. **sharepoint_client_secret**: Application Client Secret.
3. **sharepoint_tenant_id**: Microsoft 365 Tenant ID.
4. **sharepoint_tenant_name**: Organization tenant name (e.g., `myorg`).
5. **sharepoint_site_name**: SharePoint site name.


### Data Paths & Backup

6. **sharepoint_avg_backup_folder_name**: Destination folder for average data in SharePoint.
7. **sharepoint_ext_backup_folder_name**: Destination folder for extended data in SharePoint.
8. **local_backup_source_path**: Local directory used as backup source.
9. **sharepoint_backup_base_url**: Base URL for SharePoint backups.


### Location Configuration 

10. **latitude**: Latitude of the station.
11. **longitude**: Longitude of the station.

Used for georeferencing, contextual analysis, and future location-based features.


###  Task & Alert System

ECHO integrates with external services to generate alerts and manage operational tasks.

12. **bot_token**: Discord bot token used for sending alerts via the task system (e.g., Xavia Live).
13. **task_channel_id**: Discord channel ID where alerts and tasks will be posted.


### Email Notifications 

14. **email_address**: Email address used to send alerts and task notifications.
15. **email_password**: Application password (e.g., Google App Password).

> ⚠️ Note: Email delivery is currently configured for Gmail SMTP.



## Activating Debugging

If you need to debug the integration flow and view detailed results, you can enable debug logging:

1. Enable debugging directly in the Integrations UI.
2. Alternatively, add the following to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.echo: debug
```


## Inspired by

* [Meteo Lt](https://github.com/Brunas/meteo_lt)
* [AI Agent HA](https://github.com/sbenodiz/ai_agent_ha)

## EchoLib

The integration of Echo is based on the echo-lib API library. All the services that Echo offers in Home Assistant are methods defined by this API. For more information about this API, visit https://github.com/pedrozavalat/echo-lib and consult the README file.
