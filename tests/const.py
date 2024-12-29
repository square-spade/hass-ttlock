"""Dummy data for tests."""

BASIC_LOCK_DETAILS = {
    "date": 1669690212000,
    "lockAlias": "Front Door",
    "lockSound": 2,
    "modelNum": "SN9206_PV53",
    "lockMac": "16:72:4C:CC:01:C4",
    "privacyLock": 2,
    "deletePwd": "",
    "featureValue": "F44354CD5F3",
    "adminPwd": "<REMOVED>",
    "soundVolume": 5,
    "hasGateway": 1,
    "autoLockTime": 60,
    "wirelessKeypadFeatureValue": "0",
    "lockKey": "<REMOVED>",
    "isFrozen": 2,
    "lockName": "S31_c401cc",
    "resetButton": 1,
    "firmwareRevision": "6.0.6.210622",
    "tamperAlert": 1,
    "specialValue": 894227955,
    "displayPasscode": 0,
    "noKeyPwd": "<REMOVED>",
    "passageMode": 1,
    "passageModeAutoUnlock": 2,
    "timezoneRawOffset": 46800000,
    "lockId": 7252408,
    "electricQuantity": 90,
    "lockFlagPos": 0,
    "lockUpdateDate": 1682201024000,
    "keyboardPwdVersion": 4,
    "aesKeyStr": "<REMOVED>",
    "hardwareRevision": "1.6",
    "openDirection": 0,
    "lockVersion": {
        "groupId": 10,
        "protocolVersion": 3,
        "protocolType": 5,
        "orgId": 34,
        "scene": 2,
    },
    "sensitivity": -1,
}
SENSOR_LOCK_DETAILS = {
    "date": 1669690212000,
    "lockAlias": "Main Door",
    "lockSound": 1,
    "modelNum": "SN9206_PV53",
    "lockMac": "18:75:4D:CC:01:C4",
    "privacyLock": 2,
    "deletePwd": "",
    "featureValue": "10C2F44754CF5F7",
    "adminPwd": "<REMOVED>",
    "soundVolume": 1,
    "hasGateway": 1,
    "autoLockTime": -1,
    "wirelessKeypadFeatureValue": "0",
    "lockKey": "<REMOVED>",
    "isFrozen": 2,
    "lockName": "S3N_c40r",
    "resetButton": 1,
    "firmwareRevision": "6.0.6.210622",
    "tamperAlert": 1,
    "specialValue": 894227955,
    "displayPasscode": 0,
    "noKeyPwd": "<REMOVED>",
    "passageMode": 1,
    "passageModeAutoUnlock": 2,
    "timezoneRawOffset": 46800000,
    "lockId": 531507,
    "electricQuantity": 75,
    "lockFlagPos": 0,
    "lockUpdateDate": 1682201024000,
    "keyboardPwdVersion": 4,
    "aesKeyStr": "<REMOVED>",
    "hardwareRevision": "1.6",
    "openDirection": 0,
    "lockVersion": {
        "groupId": 10,
        "protocolVersion": 3,
        "protocolType": 5,
        "orgId": 34,
        "scene": 2,
    },
    "sensitivity": -1,
}

BASIC_SENSOR_DETAILS = {
    "doorSensorId": 2323,
    "name": "Door Sensor",
    "electricQuantity": 60,
    "version": "1.0.0.210903",
    "mac": "63:42:BB:C2:61:A9",
    "number": "DS2_a961c2",
}

LOCK_STATE_LOCKED = {"state": 0, "electricQuantity": 90, "lockTime": 1621459200000}

LOCK_STATE_UNLOCKED = {"state": 1, "electricQuantity": 90, "lockTime": 1621459200000}

SENSOR_STATE_OPENED = {"state": 1, "sensorState": 0, "lockTime": 1621459200000}

SENSOR_STATE_CLOSED = {"state": 0, "sensorState": 1, "lockTime": 1621459200000}

PASSAGE_MODE_6_TO_6_7_DAYS = {
    "autoUnlock": 2,
    "isAllDay": 2,
    "endDate": (6 + 12) * 60,
    "weekDays": [1, 2, 3, 4, 5, 6, 7],
    "passageMode": 1,
    "startDate": 6 * 60,
}

PASSAGE_MODE_ALL_DAY_WEEKDAYS = {
    "autoUnlock": 1,
    "isAllDay": 1,
    "weekDays": [1, 2, 3, 4, 5],
    "passageMode": 1,
}

WEBHOOK_LOCK_10AM_UTC = {
    "lockId": BASIC_LOCK_DETAILS["lockId"],
    "lockMac": BASIC_LOCK_DETAILS["lockMac"],
    "electricQuantity": 40,
    "serverDate": 1682244497000,
    "lockDate": 1682244497000,
    "recordType": 47,
    "username": "test",
    "success": 1,
}

WEBHOOK_UNLOCK_10AM_UTC = {
    "lockId": BASIC_LOCK_DETAILS["lockId"],
    "lockMac": BASIC_LOCK_DETAILS["lockMac"],
    "electricQuantity": 40,
    "serverDate": 1682244497000,
    "lockDate": 1682244497000,
    "recordType": 7,
    "username": "test",
    "success": 1,
}

WEBHOOK_OPEN_10AM_UTC = {
    "lockId": SENSOR_LOCK_DETAILS["lockId"],
    "lockMac": SENSOR_LOCK_DETAILS["lockMac"],
    "electricQuantity": 40,
    "serverDate": 1682244497000,
    "lockDate": 1682244497000,
    "recordType": 31,
    "username": "test",
    "success": 1,
}

WEBHOOK_CLOSE_10AM_UTC = {
    "lockId": SENSOR_LOCK_DETAILS["lockId"],
    "lockMac": SENSOR_LOCK_DETAILS["lockMac"],
    "electricQuantity": 40,
    "serverDate": 1682244497000,
    "lockDate": 1682244497000,
    "recordType": 30,
    "username": "test",
    "success": 1,
}
