#!/bin/bash

# call this function to write to stderr
echo_stderr ()
{
    echo "$@" >&2
}

if [ ${#} -ne 2 ]
then
    echo_stderr "Usage: load_inventory_data ${0} stage-name ${1} your-profile-name"
    exit 1
fi

export AWS_PROFILE=${2}

table_name="caring-fred-${1}-organization"
aws dynamodb put-item --table-name $table_name --item '{"address":{"S":"{\"street\": \"123 Fake Street\", \"city\": \"Fredericton\", \"country\": \"Canada\", \"postal_code\": \"A1B 2C3\", \"province\": \"NB\"}"},"administrator":{"S":"{\"first_name\": \"Howard\", \"last_name\": \"Powell\", \"email\": \"howard.powell+1@bluespurs.com\"}"},"created_at":{"S":"2018-12-05T23:04:36.553060+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-registration"},"email":{"S":"darth@vader.com"},"id":{"S":"095666f1-fae6-4c9e-b192-230efc3e31d2"},"is_verified":{"BOOL":true},"name":{"S":"Death Star"},"phone":{"S":"555-111-2222"},"updated_at":{"S":"2018-12-05T23:04:51.987717+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"}}'
aws dynamodb put-item --table-name $table_name --item '{"address":{"S":"{\"street\": \"123 Fake Street\", \"city\": \"Fredericton\", \"country\": \"Canada\", \"postal_code\": \"A1B 2C3\", \"province\": \"NB\"}"},"administrator":{"S":"{\"first_name\": \"Howard\", \"last_name\": \"Powell\", \"email\": \"howard.powell+2@bluespurs.com\"}"},"created_at":{"S":"2018-12-05T22:58:15.502232+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-registration"},"email":{"S":"admin@senate.com"},"id":{"S":"5da6a121-d783-4165-926b-ec94b81fc844"},"is_verified":{"BOOL":true},"name":{"S":"Galactic Senate"},"phone":{"S":"555-222-3333"},"updated_at":{"S":"2018-12-05T23:00:46.286815+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"}}'
aws dynamodb put-item --table-name $table_name --item '{"address":{"S":"{\"postal_code\": \"A5B 2D3\", \"country\": \"Canada\", \"province\": \"NB\", \"street\": \"121 Main Street\", \"city\": \"Moncton\"}"},"administrator":{"S":"{\"last_name\": \"Powell\", \"email\": \"howard.powell+4@bluespurs.com\", \"first_name\": \"Howard\"}"},"created_at":{"S":"2019-01-29T20:35:02.975808+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"email":{"S":"hpowell@bluepurs.com"},"id":{"S":"a57fb1db-dc26-4602-9b34-d9b37583c5b5"},"is_verified":{"BOOL":true},"name":{"S":"Test Org"},"phone":{"S":"555-222-3333"},"updated_at":{"S":"2019-01-29T20:36:05.428796+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"}}'

table_name="caring-fred-${1}-user"
aws dynamodb put-item --table-name $table_name --item '{"active":{"BOOL":true},"created_at":{"S":"2018-12-05T23:04:52.910060+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"email":{"S":"howard.powell+1@bluespurs.com"},"first_name":{"S":"Howard"},"id":{"S":"dba77332-6a8f-4631-b4e0-543063c76e42"},"last_name":{"S":"Powell"},"organization_id":{"S":"095666f1-fae6-4c9e-b192-230efc3e31d2"},"updated_at":{"S":"2018-12-05T23:04:52.910060+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"username":{"S":"howard.powell+1@bluespurs.com"}}'
aws dynamodb put-item --table-name $table_name --item '{"active":{"BOOL":true},"created_at":{"S":"2018-12-05T23:00:47.426745+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"email":{"S":"howard.powell+2@bluespurs.com"},"first_name":{"S":"Howard"},"id":{"S":"87a74264-b806-42c5-8d42-df51bcf2461f"},"last_name":{"S":"Powell"},"organization_id":{"S":"5da6a121-d783-4165-926b-ec94b81fc844"},"updated_at":{"S":"2018-12-05T23:00:47.426745+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"username":{"S":"howard.powell+2@bluespurs.com"}}'
aws dynamodb put-item --table-name $table_name --item '{"active":{"BOOL":true},"created_at":{"S":"2019-01-29T20:36:07.008387+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"email":{"S":"howard.powell+3@bluespurs.com"},"first_name":{"S":"Howard"},"id":{"S":"b85aa51d-61e7-42cd-8a6c-9baecd9177f6"},"last_name":{"S":"Powell"},"organization_id":{"S":"a57fb1db-dc26-4602-9b34-d9b37583c5b5"},"updated_at":{"S":"2019-01-29T20:36:07.008387+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"username":{"S":"howard.powell+3@bluespurs.com"}}'

table_name="caring-fred-${1}-event"
aws dynamodb put-item --table-name $table_name --item '{"categories":{"L":[]},"created_at":{"S":"2018-12-05T23:09:19.459860+0000"},"created_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1544051272"},"description":{"S":"Crush the Rebellion with one swift stroke"},"end_date":{"S":"2018-11-10"},"end_time":{"S":"16:00:00"},"id":{"S":"c5d16c0d-b572-499b-ab42-21b865d78f37"},"is_recurring":{"BOOL":false},"name":{"S":"Destroy Rebel Base"},"occurrences":{"L":[{"M":{"end_date":{"S":"2018-11-10"},"occurrence_num":{"N":"1"},"start_date":{"S":"2018-12-08"}}}]},"owner":{"S":"095666f1-fae6-4c9e-b192-230efc3e31d2"},"start_date":{"S":"2018-12-08"},"start_time":{"S":"13:00:00"},"timezone":{"S":"AST"},"updated_at":{"S":"2018-12-05T23:09:19.459860+0000"},"updated_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1544051272"}}'
aws dynamodb put-item --table-name $table_name --item '{"categories":{"L":[]},"created_at":{"S":"2018-12-05T23:07:52.803601+0000"},"created_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1544051272"},"description":{"S":"Confirm station is fully operational"},"end_date":{"S":"2018-12-09"},"end_time":{"S":"11:30:00"},"id":{"S":"cd70d122-f551-492b-b9bf-167291ef2c8d"},"is_recurring":{"BOOL":true},"name":{"S":"Test Battle Station"},"occurrences":{"L":[{"M":{"end_date":{"S":"2018-11-11"},"occurrence_num":{"N":"1"},"start_date":{"S":"2018-11-10"}}},{"M":{"end_date":{"S":"2018-11-18"},"occurrence_num":{"N":"2"},"start_date":{"S":"2018-11-17"}}},{"M":{"end_date":{"S":"2018-11-25"},"occurrence_num":{"N":"3"},"start_date":{"S":"2018-11-24"}}},{"M":{"end_date":{"S":"2018-12-02"},"occurrence_num":{"N":"4"},"start_date":{"S":"2018-12-01"}}},{"M":{"end_date":{"S":"2018-12-09"},"occurrence_num":{"N":"5"},"start_date":{"S":"2018-12-08"}}}]},"owner":{"S":"095666f1-fae6-4c9e-b192-230efc3e31d2"},"recurrence_details":{"M":{"num_recurrences":{"N":"5"},"recurrence":{"S":"WEEKLY"}}},"start_date":{"S":"2018-11-10"},"start_time":{"S":"11:00:00"},"timezone":{"S":"AST"},"updated_at":{"S":"2018-12-05T23:07:52.803601+0000"},"updated_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1544051272"}}'
aws dynamodb put-item --table-name $table_name --item '{"categories":{"L":[{"S":"scheduled"},{"S":"maintenance"}]},"created_at":{"S":"2018-12-07T14:31:15.004184+0000"},"created_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1544193075"},"description":{"S":"Check system status for errors"},"end_date":{"S":"2019-01-07"},"end_time":{"S":"17:00:00"},"id":{"S":"782790d6-a280-4ea1-bb81-07100d2d1d5c"},"is_recurring":{"BOOL":true},"name":{"S":"Check Status"},"occurrences":{"L":[{"M":{"end_date":{"S":"2018-12-10"},"occurrence_num":{"N":"1"},"start_date":{"S":"2018-12-10"}}},{"M":{"end_date":{"S":"2018-12-24"},"occurrence_num":{"N":"2"},"start_date":{"S":"2018-12-24"}}},{"M":{"end_date":{"S":"2019-01-07"},"occurrence_num":{"N":"3"},"start_date":{"S":"2019-01-07"}}}]},"owner":{"S":"095666f1-fae6-4c9e-b192-230efc3e31d2"},"recurrence_details":{"M":{"num_recurrences":{"N":"3"},"recurrence":{"S":"BI-WEEKLY"}}},"start_date":{"S":"2018-12-10"},"start_time":{"S":"15:00:00"},"timezone":{"S":"AST"},"updated_at":{"S":"2019-01-10T18:16:37.595185+0000"},"updated_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1547144197"}}'
aws dynamodb put-item --table-name $table_name --item '{"categories":{"L":[{"S":"dinner"},{"S":"charity"}]},"created_at":{"S":"2019-01-07T18:12:28.142988+0000"},"created_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1546884748"},"description":{"S":"Test event in org"},"end_date":{"S":"2018-12-10"},"end_time":{"S":"17:00:00"},"id":{"S":"142c4014-8645-4a14-a101-16fd2ae87979"},"is_recurring":{"BOOL":false},"name":{"S":"Test Event"},"occurrences":{"L":[{"M":{"end_date":{"S":"2018-12-10"},"occurrence_num":{"N":"1"},"start_date":{"S":"2018-12-10"}}}]},"owner":{"S":"a57fb1db-dc26-4602-9b34-d9b37583c5b5"},"start_date":{"S":"2018-12-10"},"start_time":{"S":"15:00:00"},"timezone":{"S":"AST"},"updated_at":{"S":"2019-01-07T18:12:28.142988+0000"},"updated_by":{"S":"AROAIOROJGONRILMNR7IC:botocore-session-1546884748"}}'
aws dynamodb put-item --table-name $table_name --item '{"categories":{"L":[{"S":"dinner"},{"S":"charity"}]},"created_at":{"S":"2019-02-19T13:40:37.405744+0000"},"created_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"},"description":{"S":"Test event in org"},"end_date":{"S":"2019-02-19"},"end_time":{"S":"17:00:00"},"id":{"S":"9d265769-1ebd-4797-9e26-5b758d888dde"},"is_recurring":{"BOOL":false},"name":{"S":"Test Event"},"occurrences":{"L":[{"M":{"end_date":{"S":"2019-02-19"},"occurrence_num":{"N":"1"},"start_date":{"S":"2019-02-19"}}}]},"owner":{"S":"a57fb1db-dc26-4602-9b34-d9b37583c5b5"},"start_date":{"S":"2019-02-19"},"start_time":{"S":"15:00:00"},"timezone":{"S":"AST"},"updated_at":{"S":"2019-02-19T13:40:37.405744+0000"},"updated_by":{"S":"AROAI3IFFH43ODT2ITRV6:caring-fred-hpowell-api"}}'