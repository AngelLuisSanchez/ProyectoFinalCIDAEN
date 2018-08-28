# ProyectoFinalCIDAEN
This project is part of the [CIDAEN course](http://www.cidaen.es/) and has been developed on the Amazon Web Services (AWS) platform through the [Serverless Framework](https://serverless.com/).

The main objective of this project is the use of AWS API Rekognition for the recognition of celebrities who appear in different Spanish newspapers. DynamoDB and S3 are used as storage systems and AWS Lambda is used as serverless media.

The visual part of the application has been developed with Angular 6, the [Chart.js framework](http://www.chartjs.org/) and the [Tag Cloud module](https://github.com/zeeshanhyder/angular-tag-cloud).

The application is deployed in a [S3 bucket](http://cidaen-proyectofinal-albertoangel.com.s3-website-eu-west-1.amazonaws.com), which acts as hosting. The project has been based on the architecture of the image.

![Architecture](https://github.com/AngelLuisSanchez/ProyectoFinalCIDAEN/blob/developer/proyectoFinalWeb/src/assets/img/cloudcraft.png)

## Requirements

### Node.Js
In order to use the Serverless Framework, it is necessary to install [Node.js](https://nodejs.org/en/) (go to the official website).

### Serverless Framework
Serverless Framework installation required: `npm install -g serverless`

In addition, two plugins are used:
* [serverless-ephemeral](https://github.com/Accenture/serverless-ephemeral)
* [serverless-pseudo-parameters](https://www.npmjs.com/package/serverless-pseudo-parameters).

To install them, run: `npm i --save-dev serverless-ephemeral` and `npm install serverless-pseudo-parameters`

### Chart.js
It has been used for displaying graphs. To install it, run: `npm install chart.js --save`

### Tag Cloud
It has been used to visualize word clouds. To install it, run: `npm install angular-tag-cloud`

## Serverless.yaml
Include plugins and include/exclude files to upload to AWS. Next, the docker image is used to install the libraries that are necessary for the process of extracting the images from the newspaper covers. These libraries are:
* requests
* beautifulsoup4
* lxml

```
plugins:
 - serverless-ephemeral
 - serverless-pseudo-parameters
package:
 exclude:
   - ./**
 include:
   - handlers/**
   - classes/**
custom:
 ephemeral:
   libraries:
   - packager:
       compose: tf-packager/docker-compose.yml
       service: packager
       output: /tmp/lambda_package.zip
```
The AWS provider, the execution environment, and a stage for development are defined. The use of apiKeys in calls to Lambda functions, where a daily limit of 50 calls has been set, to control costs when exposing this application to the public, should be highlighted.
```
provider:
 name: aws
 apiKeys:
   - ${opt:nameKeySecret}
 usagePlan:
   quota:
     limit: 50
     period: DAY
   throttle:
     burstLimit: 5
     rateLimit: 5
 runtime: python3.6
 stage: dev
 region: eu-west-1
 memorySize: 3008
 timeout: 300
```
Environment variables
```
environment:
   S3_BUCKET: inputimages-${self:provider.stage}.#{AWS::AccountId}
   DYNAMODB_TABLE: ProcessedImages-${self:provider.stage}.#{AWS::AccountId}
```
Permissions for lambda functions
```
iamRoleStatements:
   - Effect: 'Allow'
     Action:
       - 'rekognition:*'
     Resource: "*"
   - Effect: Allow
     Action:
       - s3:*
     Resource: arn:aws:s3:::${self:provider.environment.S3_BUCKET}/*
   - Effect: Allow
     Action:
       - dynamodb:Query
       - dynamodb:Scan
       - dynamodb:GetItem
       - dynamodb:PutItem
       - dynamodb:UpdateItem
       - dynamodb:DeleteItem
     Resource: "arn:aws:dynamodb:${opt:region, self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"
```
Functions that are deployed in AWS
```
functions:
 cloud-tags:
   handler: handlers/handler.get_cloud_tags
   events:
     - http:
         path: cloudtags
         method: get
         cors: true
	private: true
```
Scheduled task running for image collection
```
download-images:
   handler: handlers/handler.download_images
   events:
     - schedule: cron(00 06 * * ? *)
```
Function that is launched when an image is uploaded to S3. It's a trigger.
```
s3-new-image:
   handler: handlers/handler.image_uploaded
   events:
    - s3:
         bucket: ${self:provider.environment.S3_BUCKET}
         event: s3:ObjectCreated:*
```
Resources that are created when the application is deployed. In this case, we see how a DynamoDB table is created, with its primary and sort key.
```
resources:
 Resources:
   TodosDynamoDbTable:
     Type: 'AWS::DynamoDB::Table'
     DeletionPolicy: Retain
     Properties:
       AttributeDefinitions:
         - AttributeName: daymonthYear
           AttributeType: S
         - AttributeName: idimagen
           AttributeType: S
       KeySchema:
         - AttributeName: daymonthYear
           KeyType: HASH
         - AttributeName: idimagen
           KeyType: RANGE
       ProvisionedThroughput:
         ReadCapacityUnits: 1
         WriteCapacityUnits: 1
       TableName: ${self:provider.environment.DYNAMODB_TABLE}
```
## Deploy
To deploy the application, you need to have an AWS account and configure the Serverless Framework. We left a [quickStart](https://serverless.com/framework/docs/providers/aws/guide/quick-start/) for the process.
`serverless deploy -v --nameKeySecret keyName`
or
`sls deploy -v --nameKeySecret keyName`
