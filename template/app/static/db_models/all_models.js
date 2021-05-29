let all_models = {"api_keys": {"model": "Api_keys", "fields": {"api_key": {"dataType": "String(256)", "default": false, "nullable": false, "relationship": null, "unique": true}, "api_key_notes": {"dataType": "Text", "default": false, "nullable": true, "relationship": null, "unique": false}, "created_user_id": {"dataType": "Integer", "default": false, "nullable": false, "relationship": "user", "unique": false}, "valid_from": {"dataType": "Date", "default": false, "nullable": false, "relationship": null, "unique": false}, "valid_to": {"dataType": "Date", "default": false, "nullable": false, "relationship": null, "unique": false}}}, "hierarchies": {"model": "Hierarchies", "fields": {"organisation_id": {"dataType": "Integer", "nullable": false, "unique": false, "relationship": "organisations", "default": false}, "name": {"dataType": "String(256)", "nullable": false, "unique": false, "relationship": null, "default": false}, "path": {"dataType": "Text", "nullable": false, "unique": false, "relationship": null, "default": false}, "rank": {"dataType": "Integer", "nullable": true, "unique": false, "relationship": null, "default": false}, "parent_id": {"dataType": "Integer", "nullable": true, "unique": false, "relationship": "hierarchies", "default": false}, "key_value": {"dataType": "Text", "nullable": true, "unique": false, "relationship": null, "default": false}}}, "organisations": {"model": "Organisations", "fields": {"organisation_name": {"dataType": "String(256)", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_contact_name": {"dataType": "String(256)", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_details": {"dataType": "Text", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_contact_email": {"dataType": "String(256)", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_address": {"dataType": "Text", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_city": {"dataType": "String(256)", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_postal_code": {"dataType": "String(256)", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_country": {"dataType": "String(256)", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_homepage": {"dataType": "Text", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_vat_number": {"dataType": "Text", "nullable": true, "unique": true, "relationship": null, "default": true}, "organisation_reg_number": {"dataType": "Text", "nullable": true, "unique": true, "relationship": null, "default": true}}}}