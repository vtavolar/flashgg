import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

import FWCore.ParameterSet.VarParsing as VarParsing
from flashgg.MetaData.samples_utils import SamplesManager
from flashgg.Taggers.DiPhotonMVATrainingDumpConfNew_cff import DiPhotonMVATrainingDumpConfNew

process = cms.Process("DiPhotonMVATrainig")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_v3'
#process.GlobalTag.globaltag = 'POSTLS170_V5::All'
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
#process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring("/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-25ns/Spring15BetaV5/GluGluHToGG_M-120_13TeV_powheg_pythia8/RunIISpring15-25ns-Spring15BetaV5-v0-RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150922_093229/0000/myMicroAODOutputFile_1.root"))
process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring("/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-ReReco74X-1_1_0-25ns/1_1_0/DoubleEG/RunIISpring15-ReReco74X-1_1_0-25ns-1_1_0-v0-Run2015D-04Dec2015-v2/160112_095813/0000/myMicroAODOutputFile_1.root"))
##process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring("/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISpring15-25ns/Spring15BetaV5/GluGluHToGG_M-120_13TeV_powheg_pythia8/RunIISpring15-25ns-Spring15BetaV5-v0-RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150922_093229/0000/myMicroAODOutputFile_1.root"))
#process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring( "/store/group/phys_higgs/cmshgg/sethzenz/flashgg/HggPhys14/Phys14MicroAODV2/VBF_HToGG_M-125_13TeV-powheg-pythia6/HggPhys14-Phys14MicroAODV2-v0-Phys14DR-PU20bx25_PHYS14_25_V1-v1/150210_160130/0000/myMicroAODOutputFile_1.root"))


process.load("flashgg/Taggers/flashggTagSequence_cfi")
process.load("flashgg/Taggers/flashggPreselectedDiPhotons_cfi")
#process.load("flashgg/Systematics/flashggDiPhotonSystematics_cfi")
## process.load("flashgg/Taggers/flashggTagTester_cfi")

#from flashgg.Taggers.flashggUpdatedIdMVADiPhotons_cfi import flashggUpdatedIdMVADiPhotons
#flashggUpdatedIdMVADiPhotons.correctShowerShapes = cms.bool(False)

#from flashgg.Systematics.flashggDiPhotonSystematics_cfi import smearBins, scaleBins, smearBinsRereco, scaleBinsRereco
from flashgg.Systematics.escales.test_2016B_corr import photonSmearBins, photonScaleUncertBins 

process.flashggDiPhotonSmeared = cms.EDProducer('FlashggDiPhotonSystematicProducer',
                                        src = cms.InputTag("flashggDiPhotons"),
#                                        src = cms.InputTag("flashggUpdatedIdMVADiPhotons"),
                                        SystMethods2D = cms.VPSet(),
                                        # the number of syst methods matches the number of nuisance parameters
                                        # assumed for a given systematic uncertainty and is NOT required
                                        # to match 1-to-1 the number of bins above.
                                        SystMethods = cms.VPSet(
        cms.PSet( PhotonMethodName = cms.string("FlashggPhotonSigEoverESmearing"),
                  MethodName = cms.string("FlashggDiPhotonFromPhoton"),
                  Label = cms.string("MCSigmaEOverESmearing"),
                  NSigmas = cms.vint32(0,0),
                  OverallRange = cms.string("1"),
                  BinList = photonSmearBins,
                  ApplyCentralValue = cms.bool(True),
                  Debug = cms.untracked.bool(False)
                  ),
        cms.PSet( PhotonMethodName = cms.string("FlashggPhotonSmearConstant"),
                  MethodName = cms.string("FlashggDiPhotonFromPhoton"),
                  #Label = cms.string("MCSmearHighR9EE"),
                  Label = cms.string("MCSmear"),
                  NSigmas = cms.vint32(-1,1),
                  #OverallRange = cms.string("r9>0.94&&abs(superCluster.eta)>=1.5"),
                  OverallRange = cms.string("1"),
                  BinList = photonSmearBins,
                  ApplyCentralValue = cms.bool(True),
                  # has to match the labels embedded in the photon object as
                  # defined e.g. in flashgg/MicroAOD/python/flashggRandomizedPerPhotonDiPhotonProducer_cff.py
                  #           or in flashgg/MicroAOD/python/flashggRandomizedPhotonProducer_cff.py (if at MicroAOD prod.)
                  RandomLabel = cms.string("rnd_g_E"),
                  Debug = cms.untracked.bool(False),
                  ExaggerateShiftUp = cms.bool(False),
                                                  ),
        )
                                        )







process.flashggDiPhotonScale = cms.EDProducer('FlashggDiPhotonSystematicProducer',
                                        src = cms.InputTag("flashggDiPhotons"),
#                                        src = cms.InputTag("flashggUpdatedIdMVADiPhotons"),
                                        SystMethods2D = cms.VPSet(),
                                        # the number of syst methods matches the number of nuisance parameters
                                        # assumed for a given systematic uncertainty and is NOT required
                                        # to match 1-to-1 the number of bins above.
                                        SystMethods = cms.VPSet(
        cms.PSet( PhotonMethodName = cms.string("FlashggPhotonSigEoverESmearing"),
                  MethodName = cms.string("FlashggDiPhotonFromPhoton"),
                  Label = cms.string("DataSigmaEOverESmearing"),
                  NSigmas = cms.vint32(0,0),
                  OverallRange = cms.string("1"),
                  BinList = photonSmearBins,
                  ApplyCentralValue = cms.bool(True),
                  Debug = cms.untracked.bool(False)
                  ),
        cms.PSet( PhotonMethodName = cms.string("FlashggPhotonScale"),
                  MethodName = cms.string("FlashggDiPhotonFromPhoton"),
                  Label = cms.string("DataScale"),
                  NSigmas = cms.vint32(0,0),
                  OverallRange = cms.string("1"),
                  BinList = photonScaleUncertBins,
                  NoCentralShift = cms.bool(False),
                  ApplyCentralValue = cms.bool(True),
                  Debug = cms.untracked.bool(False)
                  )
        
        )
                                              )



#from flashgg.Taggers.flashggUpdatedIdMVADiPhotons_cfi import flashggUpdatedIdMVADiPhotons
#flashggUpdatedIdMVADiPhotons.Debug = cms.bool(False)

#process.flashggPreselectedDiPhotons.src = cms.InputTag("flashggDiPhotonSmeared")

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
#process.hltHighLevel= hltHighLevel.clone(HLTPaths = cms.vstring("HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v*", "HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v*", "HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v*") )
#process.hltHighLevel= hltHighLevel.clone(HLTPaths = cms.vstring("HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v*") )

##trigger for 2016
process.hltHighLevel= hltHighLevel.clone(HLTPaths = cms.vstring("HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v*") )


from flashgg.Taggers.flashggTagOutputCommands_cff import tagDefaultOutputCommand


process.TFileService = cms.Service("TFileService",
			fileName = cms.string("histo.root"),
			closeFileFast = cms.untracked.bool(True)
			)


process.flashggUntagged.Boundaries=cms.vdouble(-2)

# customization for job splitting, lumi weighting, etc.
from flashgg.MetaData.JobConfig import customize
customize.setDefault("maxEvents",-1)
#customize.setDefault("processIndex",5)
customize.setDefault("targetLumi",1.e+3)

#customize.setDefault("puTarget", '1.435e+05,6.576e+05,8.781e+05,1.304e+06,2.219e+06,5.052e+06,1.643e+07,6.709e+07,1.975e+08,3.527e+08,4.44e+08,4.491e+08,3.792e+08,2.623e+08,1.471e+08,6.79e+07,2.748e+07,1.141e+07,5.675e+06,3.027e+06,1.402e+06,5.119e+05,1.467e+05,3.53e+04,8270,2235,721.3,258.8,97.27,36.87,13.73,4.932,1.692,0.5519,0.1706,0.04994,0.01383,0.003627,0.0008996,0.0002111,4.689e-05,9.854e-06,1.959e-06,3.686e-07,6.562e-08,1.105e-08,1.762e-09,2.615e-10,4.768e-11,0,0,0')

#customize.setDefault("puTarget", '1.34e+05,6.34e+05,8.42e+05,1.23e+06,2.01e+06,4.24e+06,1.26e+07,4.88e+07,1.56e+08,3.07e+08,4.17e+08,4.48e+08,4.04e+08,3.05e+08,1.89e+08,9.64e+07,4.19e+07,1.71e+07,7.85e+06,4.2e+06,2.18e+06,9.43e+05,3.22e+05,8.9e+04,2.16e+04,5.43e+03,1.6e+03,551,206,80.1,31.2,11.9,4.38,1.54,0.518,0.165,0.0501,0.0144,0.00394,0.00102,0.000251,5.87e-05,1.3e-05,2.74e-06,5.47e-07,1.04e-07,1.86e-08,3.18e-09,5.16e-10,9.35e-11')
customize.setDefault("puTarget", '6.87,6.3e+03,2.79e+04,4.2e+04,7.25e+04,1.22e+05,1.46e+05,3.3e+05,8.76e+05,2.47e+06,6.24e+06,1.24e+07,2e+07,2.9e+07,3.88e+07,4.56e+07,4.74e+07,4.23e+07,3.17e+07,2.07e+07,1.3e+07,8.45e+06,5.67e+06,3.6e+06,2.03e+06,9.96e+05,4.24e+05,1.59e+05,5.65e+04,2.31e+04,1.37e+04,1.12e+04,1.01e+04,9.27e+03,8.45e+03,7.71e+03,7.08e+03,6.6e+03,6.25e+03,6.01e+03,5.85e+03,5.73e+03,5.61e+03,5.49e+03,5.34e+03,5.15e+03,4.94e+03,4.69e+03,4.41e+03,4.12e+03')

customize.options.register('diphoxml',
                           'flashgg/Taggers/data/Flashgg_DiPhoton_80x.weights.xml',
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.string,
                           'diphoxml'
                           )

customize.options.register('runOnZ',
                           '',
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.string,
                           'runOnZ'
                           )
customize.runOnZ = 'single'
customize.parse()

#move scale if it is data, smear if it MC
if customize.processType == 'data':
    process.flashggPreselectedDiPhotons.src = cms.InputTag("flashggDiPhotonScale")
    process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v8'
else:
    process.flashggPreselectedDiPhotons.src = cms.InputTag("flashggDiPhotonSmeared")
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_v3'

if customize.runOnZ != '':
    process.flashggPreselectedDiPhotons.variables[-1] = "-(passElectronVeto - 1)"
#    if customize.runOnZ == 'double':
#        process.hltHighLevel.HLTPaths = ["HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelSeedMatch_Mass70_v*"]
    if customize.runOnZ == 'single' and customize.processType == 'data':
        process.hltHighLevel.HLTPaths = ["HLT_Ele35_WPLoose_Gsf_v*"]
#    if customize.runOnZ == 'single' and customize.processType != 'data':
#        process.hltHighLevel.HLTPaths = ["HLT_Ele27_eta2p1_WP75_Gsf_v*"]

import flashgg.Taggers.dumperConfigTools as cfgTools
from flashgg.Taggers.tagsDumpers_cfi import createTagDumper
# ## FIXME switch to preselected diphotons
#process.flashggDiPhotonMVANew.DiPhotonTag = "flashggPreselectedDiPhotons"


process.tagDumper = createTagDumper("UntaggedTag")
process.tagDumper.src = "flashggUntagged"
#process.tagDumper.processIndex=cms.int32(1)
process.tagDumper.splitLumiWeight=cms.untracked.bool(True)
#process.tagDumper.throwOnUnclassified= False
process.tagDumper.dumpTrees = True
process.tagDumper.dumpWorkspace = False
process.tagDumper.quietRooFit = True


#dumpBits = ["HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95", "HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55", "HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55"]
#process.tagDumper.globalVariables.addTriggerBits = cms.PSet(
#            tag=cms.InputTag("TriggerResults","","HLT"),bits=cms.vstring(dumpBits)
#            )


process.flashggDiPhotonMVA.diphotonMVAweightfile = customize.diphoxml

#if customize.processType == 'data':
#    process.flashggDiPhotonMVA.BeamSpotSigma = -1.

minmass=100.
maxmass=180.

if customize.runOnZ:
    minmass=70.
    maxmass=120.

cfgTools.addCategory(process.tagDumper, "Reject",  "diPhoton.mass< %f || diPhoton.mass> %f" %(minmass, maxmass),
-1 ## if nSubcat is -1 do not store anythings
)

cfgTools.addCategories(process.tagDumper,
			[## cuts are applied in cascade
			("All","1",0),
			],
			variables=[
			"leadptom         := diPhotonMVA.leadptom  ",
			"subleadptom      := diPhotonMVA.subleadptom ",
			"leadmva          := diPhotonMVA.leadmva ",
			"subleadmva       := diPhotonMVA.subleadmva    ",
			"leadeta          := diPhotonMVA.leadeta     ",
			"subleadeta       := diPhotonMVA.subleadeta",
			"sigmarv          := diPhotonMVA.sigmarv",
     			"sigmawv          := diPhotonMVA.sigmawv",
			"CosPhi           := diPhotonMVA.CosPhi",
			"vtxprob          := diPhotonMVA.vtxprob",
			"result           := diPhotonMVA.result",
			"mass             := diPhoton.mass",
			"pt               := diPhoton.pt",
#                        "beamSpot         := diPhotonMVA.beamSpot",
                        "beamSpotSigZ         := diPhotonMVA.beamSpotSigZ",
                        "beamSpotX         := diPhotonMVA.beamSpotX",
                        "beamSpotY         := diPhotonMVA.beamSpotY",
                        "beamSpotZ         := diPhotonMVA.beamSpotZ",
                        "vertexz               := diPhoton().vtx().z",
                        "vertexx               := diPhoton().vtx().x",
                        "vertexy               := diPhoton().vtx().y",
                        "beamsig         := diPhotonMVA.beamsig",


                        "leadSigEoE_unsm := ? diPhoton.leadingPhoton().hasUserFloat('unsmaeraedSigmaEoE')? diPhoton.leadingPhoton().userFloat('unsmaeraedSigmaEoE'):0", 
                        "subleadSigEoE_unsm := ? diPhoton.subLeadingPhoton().hasUserFloat('unsmaeraedSigmaEoE')? diPhoton.subLeadingPhoton().userFloat('unsmaeraedSigmaEoE'):0", 
                        "dz               := ?!tagTruth().isNull()?abs(tagTruth().genPV().z-diPhoton().vtx().z):0",
                        "leadMatchType    := diPhoton.leadingPhoton().genMatchType()",
                        "subleadMatchType := diPhoton.subLeadingPhoton().genMatchType()",
                        "leadptgen := ?diPhoton.leadingPhoton().hasMatchedGenPhoton()?diPhoton.leadingPhoton().matchedGenPhoton().pt():0",
                        "subleadptgen := ?diPhoton.subLeadingPhoton().hasMatchedGenPhoton()?diPhoton.subLeadingPhoton().matchedGenPhoton().pt():0",
                        "leadSCeta    := diPhoton.leadingPhoton().superCluster().eta()",
                        "subleadSCeta    := diPhoton.subLeadingPhoton().superCluster().eta()",
                        "leadSCphi    := diPhoton.leadingPhoton().superCluster().phi()",
                        "subleadSCphi    := diPhoton.subLeadingPhoton().superCluster().phi()",
                        "leadR9    := diPhoton.leadingPhoton().r9()",
                        "subleadR9    := diPhoton.subLeadingPhoton().r9()",
                        "leadSigEOverE := diPhoton.leadingPhoton().sigEOverE()",
                        "subleadSigEOverE := diPhoton.subLeadingPhoton().sigEOverE()",
                        "massgen := diPhoton.genP4().mass()"
			],
			histograms=[
			"result>>diphoMVAValue(100,-1,1)",
			]
			)
# split tree, histogram and datasets by process
process.tagDumper.nameTemplate ="$PROCESS_$SQRTS_$LABEL"

process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True), wantSummary = cms.untracked.bool(True)  )


if customize.processType != 'data':
    process.p = cms.Path( process.tagDumper )
else:
    process.p = cms.Path( process.hltHighLevel*process.tagDumper )



customize(process)
