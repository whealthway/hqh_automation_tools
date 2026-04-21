
from .projection import PatientVisitChargeCodes
from bson import ObjectId


def get_pipeline(visitid, orguid):

    return [
        {
            "$match": {"orguid": ObjectId(orguid)}
        },
        {
            '$lookup': {
                'from': 'patientvisits',
                'localField': 'patientvisituid',
                'foreignField': '_id',
                'as': 'PatientVisit'
            }
        },
        {
            "$match": {"PatientVisit.visitid": visitid}
        },
        
        {
            '$lookup': {
                'from': 'patients',
                'localField': 'patientuid',
                'foreignField': '_id',
                'as': 'Patient'
            }
        },
        {
            '$lookup': {
                'from': 'organisations',
                'localField': 'orguid',
                'foreignField': '_id',
                'as': 'Organisation'
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'createdby',
                'foreignField': '_id',
                'as': 'CreatedBy'
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'modifiedby',
                'foreignField': '_id',
                'as': 'ModifiedBy'
            }
        },
        {
            '$unwind': '$chargecodes'
        },
        {
            '$lookup': {
                'from': 'orderitems',
                'localField': 'chargecodes.orderitemuid',
                'foreignField': '_id',
                'as': 'OrderItem'
            }
        },
        {
            '$lookup': {
                'from': 'departments',
                'localField': 'chargecodes.ordertodepartmentuid',
                'foreignField': '_id',
                'as': 'OrderToDepartment'
            }
        },
        {
            '$lookup': {
                'from': 'billinggroups',
                'localField': 'chargecodes.billinggroupuid',
                'foreignField': '_id',
                'as': 'BillingGroup'
            }
        },
        {
            '$lookup': {
                'from': 'billinggroups',
                'localField': 'chargecodes.billingsubgroupuid',
                'foreignField': '_id',
                'as': 'BillingSubGroup'
            }
        },
        {
            '$lookup': {
                'from': 'billinggroups',
                'localField': 'chargecodes.billingsubgroupuid',
                'foreignField': '_id',
                'as': 'BillingSubGroup'
            }
        },
        {
            '$project': PatientVisitChargeCodes
        }
    ]
