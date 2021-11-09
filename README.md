# PDA-STAC-Creator

## Introduction

This tool is ment to be used alongside [pda-stac-ingester](https://github.com/SatelliteApplicationsCatapult/pda-stac-ingester) 
and it is used to generate STAC metadata files and push them into an object storage.

## How can be used?

A test environment can be found in the docker-compose file that deploys *pda-stac-ingester*, *stac-fastapi* and *nats* 
server. In this scenario, PDA-STAC-Creator will be subscribed to the `stac_creator.*` topic and will publish to 
`stac_ingester.*` when a new created STAC metadata has been created, and it is ready to be ingested.

Using [nats-cli](https://github.com/nats-io/natscli) from localhost, and assuming the whole environment has been 
deployed using docker-compose:

### Creating a Catalog

It will attempt to creating a new Catalog on the given `S3_STAC_KEY`. If there is a catalog.json file within that location
already, it will consider the generated collections as part of it.


### Creating a Collection

```bash
nats pub -s nats://localhost:4222 stac_creator.collection stac_catalogs/novasar_test/novasar_scansar_20m/collection.json
```

### Creating an Item

```bash
nats pub -s nats://localhost:4222 stac_creator.item stac_catalogs/novasar_test/novasar_scansar_20m/NovaSAR_01_16359_slc_11_201025_231831_HH_2_ML_TC_TF_cog/NovaSAR_01_16359_slc_11_201025_231831_HH_2_ML_TC_TF_cog.json
```

**NOTE**: This example is using the *https://s3-uk-1.sa-catapult.co.uk* endpoint and *public-eo-data* bucket given by 
environmental variables within the docker-compose file. The tool will receive this as part of the deployment process and
assumes the objects are available through https without authentication.