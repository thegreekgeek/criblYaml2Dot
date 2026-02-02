
Use the Cribl API to programmatically update the configuration of supported objects like Sources and Destinations. Use the `/system/inputs` endpoints for Sources and the `/system/outputs` endpoints for Destinations (see the [API Reference](/api-reference/) for details).

> ##### About the Example Requests {{< id `about-api-examples` >}}
>
> Replace the variables in the example requests with the corresponding information for your Cribl deployment. In the cURL command options, replace `${token}` with a valid [API Bearer token](api-auth). You can also set the `$token` environment variable to match the value of a Bearer token.
>
> For on-prem deployments, to use `https` in the URL for your requests as shown in these examples, you must [configure Transport Layer Security (TLS)](/stream/securing-tls/).
>
> In Cribl.Cloud and other distributed deployments, you must **commit** and **deploy** the changes you make. You can use the Cribl API to [automate commit and deploy commands](commit-deploy).
>
{.box .info}

## Update a Destination Configuration {#update-destination}

This example demonstrates how to change the secret key pair that is used to authenticate to an existing MinIO Destination by sending a `PATCH` request to the `/system/outputs/{id}` endpoint. But first, you'll send a `GET` request to retrieve the definition for the Destination. The definition includes the attributes and values you'll need to include in the body of your `PATCH` request.

> The `PATCH /system/outputs/{id}` endpoint requires a **complete** representation of the resource that you want to update in the request body. This endpoint does not support partial updates. Cribl removes any omitted fields when updating the resource.
>
> Also, the body for your `PATCH` request is based on the existing configuration that you [retrieve](#get-destination-definition), so you must confirm that the configuration is correct. If the existing configuration is incorrect, the updated resource may not function as expected.
>
{.box .warning}

### 1. Retrieve the Definition for the Destination {#get-destination-definition}

Retrieve the definition for the Destination that you want to update. After you confirm that the retrieved definition is correct, you'll use it as the basis of your request in the next step, changing only the values that you want to update.

In this example, the Destination ID is `MinIO_testing`.

{{% tabs "cloud" "cloud" "Cribl.Cloud and Hybrid" "single" "On-Prem (Single-Instance)" "dist" "On-Prem (Distributed)" %}}
{{% tab-item "cloud" %}}

```shell
curl --request GET \
--url 'https://${workspaceName}-${organizationId}.cribl.cloud/api/v1/m/${groupName}/system/outputs/MinIO_testing' \
--header 'Authorization: Bearer ${token}' \
--header 'Content-Type: application/json'
```

{{% /tab-item %}}
{{% tab-item "single" %}}

```shell
curl --request GET \
--url 'https://${hostname}:${port}/api/v1/system/outputs/MinIO_testing' \
--header 'Authorization: Bearer ${token}' \
--header 'Content-Type: application/json'
```

{{% /tab-item %}}
{{% tab-item "dist" %}}

```shell
curl --request GET \
--url 'https://${hostname}:${port}/api/v1/m/${groupName}/system/outputs/MinIO_testing' \
--header 'Authorization: Bearer ${token}' \
--header 'Content-Type: application/json'
```

{{% /tab-item %}}
{{% /tabs %}}

The response includes the definition of the `MinIO_testing` Destination as a JSON object:

```json
{
  "items": [
    {
      "id": "MinIO_testing",
      "systemFields": [
        "cribl_pipe"
      ],
      "streamtags": [],
      "awsAuthenticationMethod": "secret",
      "stagePath": "$CRIBL_HOME/state/outputs/testing",
      "addIdToStagePath": true,
      "signatureVersion": "v4",
      "objectACL": "private",
      "reuseConnections": true,
      "rejectUnauthorized": true,
      "verifyPermissions": true,
      "removeEmptyDirs": true,
      "partitionExpr": "C.Time.strftime(_time ? _time : Date.now()/1000, '%Y/%m/%d')",
      "format": "json",
      "baseFileName": "`CriblOut`",
      "fileNameSuffix": "`.${C.env[\"CRIBL_WORKER_ID\"]}.${__format}${__compression === \"gzip\" ? \".gz\" : \"\"}`",
      "maxFileSizeMB": 32,
      "maxOpenFiles": 100,
      "headerLine": "",
      "writeHighWaterMark": 64,
      "onBackpressure": "block",
      "deadletterEnabled": false,
      "onDiskFullBackpressure": "block",
      "maxFileOpenTimeSec": 300,
      "maxFileIdleTimeSec": 30,
      "maxConcurrentFileParts": 4,
      "compress": "gzip",
      "compressionLevel": "best_speed",
      "emptyDirCleanupSec": 300,
      "type": "minio",
      "endpoint": "http://minio:9090",
      "bucket": "test",
      "awsSecret": "MinIO_testing_minio_secret_keypair",
      "status": {
        "health": "Green",
        "timestamp": 1742219848827,
        "metrics": {
          "openFileStreams": 0,
          "sentCount": 0,
          "bytesWritten": 0
        }
      },
      "notifications": []
    }
  ],
  "count": 1
}
```

### 2. Update the Destination Configuration {#update-destination-config}

Use the response to the `GET /system/outputs/{id}` request from the previous step as the request body, with the following changes:

   - Do not include the `items` array or the `count` attribute from the `GET` response.
   - Replace the value for the `awsSecret` parameter with the name of the secret key pair that you want to use for the Destination.

> Do not omit any fields from the resource representation in the request body. Include a complete representation of the resource, replacing only the values for the fields that you want to update. Cribl removes any omitted fields when updating the resource.
>
{.box .info}

{{% tabs "cloud" "cloud" "Cribl.Cloud and Hybrid" "single" "On-Prem (Single-Instance)" "dist" "On-Prem (Distributed)" %}}
{{% tab-item "cloud" %}}

```shell
curl --request PATCH \
--url 'https://${workspaceName}-${organizationId}.cribl.cloud/api/v1/m/${groupName}/system/outputs/MinIO_testing' \
--header 'Authorization: Bearer ${token}' \
--header 'Content-Type: application/json' \
--data '{
  "id": "MinIO_testing",
  "systemFields": [
      "cribl_pipe"
  ],
  "streamtags": [],
  "awsAuthenticationMethod": "secret",
  "stagePath": "$CRIBL_HOME/state/outputs/testing",
  "addIdToStagePath": true,
  "signatureVersion": "v4",
  "objectACL": "private",
  "reuseConnections": true,
  "rejectUnauthorized": true,
  "verifyPermissions": true,
  "removeEmptyDirs": true,
  "partitionExpr": "C.Time.strftime(_time ? _time : Date.now()/1000, '%Y/%m/%d')",
  "format": "json",
  "baseFileName": "`CriblOut`",
  "fileNameSuffix": "`.${C.env[\"CRIBL_WORKER_ID\"]}.${__format}${__compression === \"gzip\" ? \".gz\" : \"\"}`",
  "maxFileSizeMB": 32,
  "maxOpenFiles": 100,
  "headerLine": "",
  "writeHighWaterMark": 64,
  "onBackpressure": "block",
  "deadletterEnabled": false,
  "onDiskFullBackpressure": "block",
  "maxFileOpenTimeSec": 300,
  "maxFileIdleTimeSec": 30,
  "maxConcurrentFileParts": 4,
  "compress": "gzip",
  "compressionLevel": "best_speed",
  "emptyDirCleanupSec": 300,
  "type": "minio",
  "endpoint": "http://minio:9090",
  "bucket": "test",
  "awsSecret": "MinIO_new_minio_secret_keypair",
  "status": {
      "health": "Green",
      "timestamp": 1742222265527,
      "metrics": {
          "openFileStreams": 0,
          "sentCount": 0,
          "bytesWritten": 0
      }
  },
  "notifications": []
}'
```

{{% /tab-item %}}
{{% tab-item "single" %}}

```shell
curl --request PATCH \
--url 'https://${hostname}:${port}/api/v1/system/outputs/MinIO_testing' \
--header 'Authorization: Bearer ${token}' \
--header 'Content-Type: application/json' \
--data '{
  "id": "MinIO_testing",
  "systemFields": [
      "cribl_pipe"
  ],
  "streamtags": [],
  "awsAuthenticationMethod": "secret",
  "stagePath": "$CRIBL_HOME/state/outputs/testing",
  "addIdToStagePath": true,
  "signatureVersion": "v4",
  "objectACL": "private",
  "reuseConnections": true,
  "rejectUnauthorized": true,
  "verifyPermissions": true,
  "removeEmptyDirs": true,
  "partitionExpr": "C.Time.strftime(_time ? _time : Date.now()/1000, '%Y/%m/%d')",
  "format": "json",
  "baseFileName": "`CriblOut`",
  "fileNameSuffix": "`.${C.env[\"CRIBL_WORKER_ID\"]}.${__format}${__compression === \"gzip\" ? \".gz\" : \"\"}`",
  "maxFileSizeMB": 32,
  "maxOpenFiles": 100,
  "headerLine": "",
  "writeHighWaterMark": 64,
  "onBackpressure": "block",
  "deadletterEnabled": false,
  "onDiskFullBackpressure": "block",
  "maxFileOpenTimeSec": 300,
  "maxFileIdleTimeSec": 30,
  "maxConcurrentFileParts": 4,
  "compress": "gzip",
  "compressionLevel": "best_speed",
  "emptyDirCleanupSec": 300,
  "type": "minio",
  "endpoint": "http://minio:9090",
  "bucket": "test",
  "awsSecret": "MinIO_new_minio_secret_keypair",
  "status": {
      "health": "Green",
      "timestamp": 1742222265527,
      "metrics": {
          "openFileStreams": 0,
          "sentCount": 0,
          "bytesWritten": 0
      }
  },
  "notifications": []
}'
```

{{% /tab-item %}}
{{% tab-item "dist" %}}

```shell
curl --request PATCH \
--url 'https://${hostname}:${port}/api/v1/m/${groupName}/system/outputs/MinIO_testing' \
--header 'Authorization: Bearer ${token}' \
--header 'Content-Type: application/json' \
--data '{
  "id": "MinIO_testing",
  "systemFields": [
      "cribl_pipe"
  ],
  "streamtags": [],
  "awsAuthenticationMethod": "secret",
  "stagePath": "$CRIBL_HOME/state/outputs/testing",
  "addIdToStagePath": true,
  "signatureVersion": "v4",
  "objectACL": "private",
  "reuseConnections": true,
  "rejectUnauthorized": true,
  "verifyPermissions": true,
  "removeEmptyDirs": true,
  "partitionExpr": "C.Time.strftime(_time ? _time : Date.now()/1000, '%Y/%m/%d')",
  "format": "json",
  "baseFileName": "`CriblOut`",
  "fileNameSuffix": "`.${C.env[\"CRIBL_WORKER_ID\"]}.${__format}${__compression === \"gzip\" ? \".gz\" : \"\"}`",
  "maxFileSizeMB": 32,
  "maxOpenFiles": 100,
  "headerLine": "",
  "writeHighWaterMark": 64,
  "onBackpressure": "block",
  "deadletterEnabled": false,
  "onDiskFullBackpressure": "block",
  "maxFileOpenTimeSec": 300,
  "maxFileIdleTimeSec": 30,
  "maxConcurrentFileParts": 4,
  "compress": "gzip",
  "compressionLevel": "best_speed",
  "emptyDirCleanupSec": 300,
  "type": "minio",
  "endpoint": "http://minio:9090",
  "bucket": "test",
  "awsSecret": "MinIO_new_minio_secret_keypair",
  "status": {
      "health": "Green",
      "timestamp": 1742222265527,
      "metrics": {
          "openFileStreams": 0,
          "sentCount": 0,
          "bytesWritten": 0
      }
  },
  "notifications": []
}'
```

{{% /tab-item %}}
{{% /tabs %}}

The response includes the definition of the `MinIO_testing` Destination with the updated `awsSecret` value:

```json
{
  "items": [
    {
      "id": "MinIO_testing",
      "systemFields": [
        "cribl_pipe"
      ],
      "streamtags": [],
      "awsAuthenticationMethod": "secret",
      "stagePath": "$CRIBL_HOME/state/outputs/testing",
      "addIdToStagePath": true,
      "signatureVersion": "v4",
      "objectACL": "private",
      "reuseConnections": true,
      "rejectUnauthorized": true,
      "verifyPermissions": true,
      "removeEmptyDirs": true,
      "partitionExpr": "C.Time.strftime(_time ? _time : Date.now()/1000, '%Y/%m/%d')",
      "format": "json",
      "baseFileName": "`CriblOut`",
      "fileNameSuffix": "`.${C.env[\"CRIBL_WORKER_ID\"]}.${__format}${__compression === \"gzip\" ? \".gz\" : \"\"}`",
      "maxFileSizeMB": 32,
      "maxOpenFiles": 100,
      "headerLine": "",
      "writeHighWaterMark": 64,
      "onBackpressure": "block",
      "deadletterEnabled": false,
      "onDiskFullBackpressure": "block",
      "maxFileOpenTimeSec": 300,
      "maxFileIdleTimeSec": 30,
      "maxConcurrentFileParts": 4,
      "compress": "gzip",
      "compressionLevel": "best_speed",
      "emptyDirCleanupSec": 300,
      "type": "minio",
      "endpoint": "http://minio:9090",
      "bucket": "test",
      "awsSecret": "MinIO_new_minio_secret_keypair",
      "notifications": [],
      "status": {
        "health": "Green",
        "timestamp": 1742223031723,
        "metrics": {
          "openFileStreams": 0,
          "sentCount": 0,
          "bytesWritten": 0
        }
      }
    }
  ],
  "count": 1
}
```
