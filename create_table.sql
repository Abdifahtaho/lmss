CREATE TABLE "land_management_passwordresetrequest" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "requested_at" datetime NOT NULL,
    "status" varchar(10) NOT NULL,
    "processed_at" datetime NULL,
    "processed_by_id" integer NULL REFERENCES "auth_user" ("id"),
    "rejection_reason" text NULL
); 