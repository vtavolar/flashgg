import FWCore.ParameterSet.Config as cms

flashggUpdatedIdMVADiPhotons = cms.EDProducer("FlashggDiPhotonWithUpdatedPhoIdMVAProducer",
                                              src=cms.InputTag("flashggDiPhotons"),
                                              rhoFixedGridCollection = cms.InputTag('fixedGridRhoAll'),
                                              photonIdMVAweightfile_EB = cms.FileInPath("flashgg/MicroAOD/data/MVAweights_76X_25ns_r9s4EtaWshift_barrel.xml"),
                                              photonIdMVAweightfile_EE = cms.FileInPath("flashgg/MicroAOD/data/MVAweights_76X_25ns_endcap.xml"),
                                              showerShapeTransfFile = cms.FileInPath("flashgg/Taggers/data/transformation_76X_v2.root"),
                                              correctShowerShapes = cms.bool(False),
                                              Debug=cms.bool(False)
                                              )
