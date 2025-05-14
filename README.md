# SAVIIA 
### *Sistema de Administración y Visualización de Información para la Investigación y Análisis*

Home Assistant integration for remote data extraction at the UC Patagonia Research Center.

![SAVIIA](images/icon.png)


## Installation via HACS

1. The **SAVIIA integration** is not part of the HACS Store. To install it, you will need to add it as a *custom repository* by following this guide: [HACS Custom Repositories](https://hacs.xyz/docs/faq/custom_repositories/).
2. Download the integration by entering the repository URL and adding it. Then, go to HACS and install it.
3. Once the installation is complete, **restart** Home Assistant.
4. After restarting, navigate to the **Integrations page** to configure the service.

## Service Configuration

To export files from the THIES Data Logger DL16 station to a folder in Microsoft SharePoint, you will need to enter the following credentials, which will be requested in the configuration form:

1. **ftp\_host**: The IP address of the FTP server.
2. **ftp\_port**: The FTP server's port (usually 21).
3. **ftp\_user**: The FTP server's username.
4. **ftp\_password**: The FTP server's password.
5. **sharepoint\_client\_id** and **sharepoint\_client\_secret**: The Client ID and Client Secret of your Microsoft SharePoint application. You must have already created an application and obtained the necessary permissions.
6. **sharepoint\_tenant\_id**: The SharePoint Tenant ID (the global identifier for your organization's domain in Microsoft 365).
7. **sharepoint_tenant_name** and **sharepoint_site_name**: The name of your organization’s SharePoint site. For example, for the URL `https://myorg.sharepoint.com/sites/myorg365_NameOfMyApplication`, if your tenant name is `myorg` and your site name is `myorg365_NameOfMyApplication`, you would enter these values accordingly.



## Activating Debugging

If you need to debug the integration flow and view detailed results, you can enable debug logging:

1. Enable debugging directly in the Integrations UI.
2. Alternatively, add the following to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.saviia: debug
```

## Inspired by

- [Meteo Lt](https://github.com/Brunas/meteo_lt)  
