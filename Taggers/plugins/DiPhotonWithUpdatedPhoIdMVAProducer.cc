#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "flashgg/MicroAOD/interface/PhotonIdUtils.h"
#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"
#include "TGraph.h"
#include "TFile.h"


namespace flashgg {

    class DiPhotonWithUpdatedPhoIdMVAProducer : public edm::EDProducer
    {
    public:
        DiPhotonWithUpdatedPhoIdMVAProducer( const edm::ParameterSet & );
        void produce( edm::Event &, const edm::EventSetup & ) override;

    private:
        edm::EDGetTokenT<edm::View<flashgg::DiPhotonCandidate> > token_;
        edm::EDGetTokenT<double> rhoToken_;
        PhotonIdUtils phoTools_;
        edm::FileInPath phoIdMVAweightfileEB_, phoIdMVAweightfileEE_;
        bool debug_;
        bool correctShowerShapes_;
        edm::FileInPath showerShapeTransfFile_ ;
    };

    DiPhotonWithUpdatedPhoIdMVAProducer::DiPhotonWithUpdatedPhoIdMVAProducer( const edm::ParameterSet &ps ) :
        token_(consumes<edm::View<flashgg::DiPhotonCandidate> >(ps.getParameter<edm::InputTag>("src"))),
        rhoToken_( consumes<double>( ps.getParameter<edm::InputTag>( "rhoFixedGridCollection" ) ) ),
        debug_( ps.getParameter<bool>( "Debug" ) )
    {
        correctShowerShapes_ =  ps.exists("correctShowerShapes") ? ( ps.getParameter<bool>( "correctShowerShapes" )) : false  ;
        phoIdMVAweightfileEB_ = ps.getParameter<edm::FileInPath>( "photonIdMVAweightfile_EB" );
        phoIdMVAweightfileEE_ = ps.getParameter<edm::FileInPath>( "photonIdMVAweightfile_EE" );
        showerShapeTransfFile_ = ps.getParameter<edm::FileInPath>( "showerShapeTransfFile" );
        phoTools_.setupMVA( phoIdMVAweightfileEB_.fullPath(), phoIdMVAweightfileEE_.fullPath() );

        produces<std::vector<flashgg::DiPhotonCandidate> >();
    }

    void DiPhotonWithUpdatedPhoIdMVAProducer::produce( edm::Event &evt, const edm::EventSetup & )
    {
        edm::Handle<edm::View<flashgg::DiPhotonCandidate> > objects;
        evt.getByToken( token_, objects );

        edm::Handle<double> rhoHandle;
        evt.getByToken( rhoToken_, rhoHandle );
        const double rhoFixedGrd = *( rhoHandle.product() );

        auto_ptr<std::vector<flashgg::DiPhotonCandidate> > out_obj( new std::vector<flashgg::DiPhotonCandidate>() );


        TFile* f_corr = TFile::Open( showerShapeTransfFile_.fullPath().c_str() );
        TGraph* gEWEB = (TGraph*) f_corr->Get("transfEtaWidthEB");
        TGraph* gS4EB = (TGraph*) f_corr->Get("transfS4EB");
        TGraph* gR9full5x5EB = (TGraph*) f_corr->Get("transffull5x5R9EB");
        float uncorrEW=0., uncorrS4=0., uncorrR9=0.;

        for (const auto & obj : *objects) {
            if (this->debug_) {
                std::cout << " Input DiPhoton lead (sublead) MVA: " << obj.leadPhotonId() << " " << obj.subLeadPhotonId() << std::endl;
            }
            flashgg::DiPhotonCandidate *new_obj = obj.clone();
            new_obj->makePhotonsPersistent();
            if(correctShowerShapes_){

                if(new_obj->getLeadingPhoton().isEB()){
                    if (this->debug_){
                        std::cout<<"Before transformation, leading: R9  S4  EW"<<std::endl;
                        std::cout<<new_obj->getLeadingPhoton().correctedR9()<<"  "<<new_obj->getLeadingPhoton().correctedS4()<<"  "<<new_obj->getLeadingPhoton().correctedEtaWidth()<<std::endl;
                        std::cout<<new_obj->getLeadingPhoton().full5x5_r9()<<"  "<<new_obj->getLeadingPhoton().s4()<<"  "<<new_obj->getLeadingPhoton().superCluster()->etaWidth()<<std::endl;
                        
                    }
                    uncorrEW = new_obj->getLeadingPhoton().superCluster()->etaWidth();
                    uncorrS4 = new_obj->getLeadingPhoton().s4();
                    uncorrR9 = new_obj->getLeadingPhoton().full5x5_r9() ;
                    new_obj->getLeadingPhoton().setcorrectedR9( gR9full5x5EB->Eval( uncorrR9  )    );
                    new_obj->getLeadingPhoton().setcorrectedS4( gS4EB->Eval( uncorrS4  )    );
                    new_obj->getLeadingPhoton().setcorrectedEtaWidth( gEWEB->Eval( uncorrEW  )    );
                    if (this->debug_){
                        std::cout<<"After transformation, leading: R9  S4  EW"<<std::endl;
                        std::cout<<new_obj->getLeadingPhoton().correctedR9()<<"  "<<new_obj->getLeadingPhoton().correctedS4()<<"  "<<new_obj->getLeadingPhoton().correctedEtaWidth()<<std::endl;
                        std::cout<<new_obj->getLeadingPhoton().full5x5_r9()<<"  "<<new_obj->getLeadingPhoton().s4()<<"  "<<new_obj->getLeadingPhoton().superCluster()->etaWidth()<<std::endl;
                    }
                }
                if(new_obj->getSubLeadingPhoton().isEB()){
                    if (this->debug_){
                        std::cout<<"Before transformation, subleading: R9  S4  EW"<<std::endl;
                        std::cout<<new_obj->getSubLeadingPhoton().correctedR9()<<"  "<<new_obj->getSubLeadingPhoton().correctedS4()<<"  "<<new_obj->getSubLeadingPhoton().correctedEtaWidth()<<std::endl;
                        std::cout<<new_obj->getSubLeadingPhoton().full5x5_r9()<<"  "<<new_obj->getSubLeadingPhoton().s4()<<"  "<<new_obj->getSubLeadingPhoton().superCluster()->etaWidth()<<std::endl;
                    }
                    uncorrEW = new_obj->getSubLeadingPhoton().superCluster()->etaWidth();
                    uncorrS4 = new_obj->getSubLeadingPhoton().s4();
                    uncorrR9 = new_obj->getSubLeadingPhoton().full5x5_r9() ;
                    new_obj->getSubLeadingPhoton().setcorrectedR9( gR9full5x5EB->Eval( uncorrR9  )    );
                    new_obj->getSubLeadingPhoton().setcorrectedS4( gS4EB->Eval( uncorrS4  )    );
                    new_obj->getSubLeadingPhoton().setcorrectedEtaWidth( gEWEB->Eval( uncorrEW  )    );
                    if (this->debug_){
                        std::cout<<"After transformation, subleading: R9  S4  EW"<<std::endl;
                        std::cout<<new_obj->getSubLeadingPhoton().correctedR9()<<"  "<<new_obj->getSubLeadingPhoton().correctedS4()<<"  "<<new_obj->getSubLeadingPhoton().correctedEtaWidth()<<std::endl;
                        std::cout<<new_obj->getSubLeadingPhoton().full5x5_r9()<<"  "<<new_obj->getSubLeadingPhoton().s4()<<"  "<<new_obj->getSubLeadingPhoton().superCluster()->etaWidth()<<std::endl;
                    }
                }

            }

            float newleadmva = phoTools_.computeMVAWrtVtx( new_obj->getLeadingPhoton(), new_obj->vtx(), rhoFixedGrd );
            new_obj->getLeadingPhoton().setPhoIdMvaWrtVtx( new_obj->vtx(), newleadmva);
            float newsubleadmva = phoTools_.computeMVAWrtVtx( new_obj->getSubLeadingPhoton(), new_obj->vtx(), rhoFixedGrd );
            new_obj->getSubLeadingPhoton().setPhoIdMvaWrtVtx( new_obj->vtx(), newsubleadmva);
            if (this->debug_) {
                std::cout << " Output DiPhoton lead (sublead) MVA: " << new_obj->leadPhotonId() << " " << new_obj->subLeadPhotonId() << std::endl;
            }
            out_obj->push_back(*new_obj);
        }
        delete f_corr;
        delete gEWEB;
        delete gS4EB;
        delete gR9full5x5EB;
        evt.put(out_obj);
    }
}

typedef flashgg::DiPhotonWithUpdatedPhoIdMVAProducer FlashggDiPhotonWithUpdatedPhoIdMVAProducer;
DEFINE_FWK_MODULE( FlashggDiPhotonWithUpdatedPhoIdMVAProducer );

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
