"""Wrapper for the DICOM integration."""
from pydicom import dcmread
from pydicom.dataset import Dataset as DS
from pynetdicom import (
    AE as AppEntity, BasicWorklistManagementPresentationContexts,
    QueryRetrievePresentationContexts, StoragePresentationContexts,
    VerificationPresentationContexts)


class AE(AppEntity):
    """Wrapper for the DICOM app entity."""
    pass


class Dataset(DS):
    """Wrapper for the DICOM dataset."""
    pass
