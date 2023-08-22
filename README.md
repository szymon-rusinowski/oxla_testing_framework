# README #

## To Login
curl -k -v -X POST -H 'Content-type: application/x-www-form-urlencoded' -d 'username=admin&password=Test123' http://localhost:8000/api/v1/soileo_api/login

### example_response:
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY3MzU0MTkzOX0.O4W610fNieBkJ9kfAbiOejuVghXwh2waul2Be_PCPqE","token_type":"bearer"}

### To process below request copy access_token after "Bearer "

### Use access token in further request after login for further requests

## To insert client shape
curl -X POST -H "Content-Type: Application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY3MzYxMTU5Mn0.BSClU9E0kk8rtMOYbIQogjL9qmXLWOJHTZOJmwPKyHA" -d '{"geojson_path":"admin_test.geojson","area_name":"test"}' http://localhost:8000/api/v1/soileo_api/insert_shape

## To insert hsi shape
curl -X POST -H "Content-Type: Application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY3MzYxMzQ0MX0.XlMsUz8o4DGYauqOkC0IoZihVU0r9oD25Xf5EqgzEUc" -d '{"geojson_path":"glucholazy_2022_3.geojson","specific_name":"glucholazy", "hsi_path": "wynik_3.dat", "month":3, "year":2022}' http://localhost:8000/api/v1/soileo_api/insert_hsi_shape

## To query available shapes
icurl -X GET -H "Content-Type: Application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY3MzYyOTQ1Nn0.uLbo-Ol3i7sberGuZzaMEc6nrzIAz39CgruUV31MgQQ" -d '{"shape_name": "fake_name"}' http://localhost:8000/api/v1/soileo_api/overlaping_hsi

### example response
{"data":[{"area_name":"Test","hsi_paths":"wynik_3.dat","month":"03","year":"2022"},{"area_name":"glucholazy","hsi_paths":"wynik_3.dat","month":"3","year":"2022"}],"success":true}

## To run inference with dataset building
curl -X GET -H "Content-Type: Application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY3MzYzMzQ3OX0.bmfaq_iGImCGfuMi72QLcqOnv0sdTmrtlaHA7nN6g10" -d '{"year":2022, "month": 3, "shape_name": "name", "hsi_paths": ["wynik_3.dat"], "grid_path": "grid.geojson", "elements":["P", "K", "pH"]}' http://localhost:8000/api/v1/soileo_api/inference_data
