
from .projection import PatientVisitOrders
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
                'from': 'referencevalues',
                'localField': 'entypeuid',
                'foreignField': '_id',
                'as': 'EncounterType'
            }
        },
        {
            '$lookup': {
                'from': 'inventorystores',
                'localField': 'invstoreuid',
                'foreignField': '_id',
                'as': 'Store'
            }
        },
        {
            '$lookup': {
                'from': 'departments',
                'localField': 'orderdepartmentuid',
                'foreignField': '_id',
                'as': 'OrderDepartment'
            }
        },
        {
            '$lookup': {
                'from': 'departments',
                'localField': 'ordertodepartmentuid',
                'foreignField': '_id',
                'as': 'OrderToDepartment'
            }
        },
        {
            '$lookup': {
                'from': 'referencevalues',
                'localField': 'bedcategoryuid',
                'foreignField': '_id',
                'as': 'BedCat'
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
            '$unwind': '$patientorderitems'
        },
        {
            '$lookup': {
                'from': 'orderitems',
                'localField': 'patientorderitems.orderitemuid',
                'foreignField': '_id',
                'as': 'OrderItem'
            }
        },
        {
            '$lookup': {
                'from': 'ordersets',
                'localField': 'patientorderitems.ordersetuid',
                'foreignField': '_id',
                'as': 'OrderSet'
            }
        },
        {
            '$lookup': {
                'from': 'ordercategories',
                'localField': 'patientorderitems.ordercatuid',
                'foreignField': '_id',
                'as': 'OrderCategory'
            }
        },
        {
            '$lookup': {
                'from': 'ordercategories',
                'localField': 'patientorderitems.ordersubcatuid',
                'foreignField': '_id',
                'as': 'OrderSubCategory'
            }
        },
        {
            '$lookup': {
                'from': 'tariffs',
                'localField': 'patientorderitems.tariffuid',
                'foreignField': '_id',
                'as': 'Tariff'
            }
        },
        {
            '$lookup': {
                'from': 'billinggroups',
                'localField': 'patientorderitems.billinggroupuid',
                'foreignField': '_id',
                'as': 'BillingGroup'
            }
        },
        {
            '$lookup': {
                'from': 'billinggroups',
                'localField': 'patientorderitems.billingsubgroupuid',
                'foreignField': '_id',
                'as': 'BillingSubGroup'
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'patientorderitems.careprovideruid',
                'foreignField': '_id',
                'as': 'CareProvider'
            }
        },
        {
            '$lookup': {
                'from': 'referencevalues',
                'localField': 'patientorderitems.statusuid',
                'foreignField': '_id',
                'as': 'Status'
            }
        },
        {
            '$lookup': {
                'from': 'referencevalues',
                'localField': 'patientorderitems.quantityUOM',
                'foreignField': '_id',
                'as': 'QuantityUOM'
            }
        },
        {
            '$project': PatientVisitOrders
        },
    ]
