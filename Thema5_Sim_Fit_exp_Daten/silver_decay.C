// Elektronenstreuung in Materie

// #include<iostream>
// #include<fstream>
#include<math.h>

// constants

const Double_t pi = TMath::Pi();   // pi
const Double_t me = 0.511;         // electron mass [MeV]

const Int_t N_ELEC = 50;           // number of electrons
const Double_t X_MAX = 100;        // x-size of the detector
const Double_t Y_MAX = 100;        // y-size of the detector
const Double_t E_0 = 20;           // energy of electrons
const Double_t E_MIN = 0.02;       // minimum energy of electrons
//TF1 *f_theta;
TF1 *f_phi;
TF1 *f_length;
TF1 *f_moll;
TF1 *f_mott;
TRandom *r2 = new TRandom2();
 
class electron: public TObject {
public :
  electron(Double_t x1, Double_t y1, Double_t z1, Double_t E1 , Double_t theta1, Double_t phi1);
  ~electron();
  Double_t x;
  Double_t y;
  Double_t z;
  Double_t E;
  Double_t theta;
  Double_t phi;
};

electron::electron(Double_t x1, Double_t y1, Double_t z1, Double_t E1 , Double_t theta1, Double_t phi1) {
  x=x1; y=y1; z=z1; E=E1; theta=theta1; phi=phi1;}

electron::~electron(){};

Int_t nextcoord(electron *e1, electron *e2) 
{

// Keep starting position of struck electron e2

    e2->x = e1->x;
    e2->y = e1->y;
    e2->z = e1->z;
    Double_t otheta = e1->theta;  // old theta
    Double_t ophi   = e1->phi;    // old phi
    Double_t p1;
    Double_t p2;
    Double_t theta1;
    Double_t theta2;

// calculate new coordinates

// Moeller scattering
//    Double_t n_theta = f_theta->GetRandom();

    Double_t n_phi = f_phi->GetRandom();
    Double_t len= f_length->GetRandom()*pow(e1->E/1,2)/50; // scattering length (scales with 1/E^2)
    
    //    cout << "th, phi, len, E:" << n_theta << " " << n_phi << " " << len << " " << e1->E << endl;
    Double_t p = sqrt(pow(e1->E+me,2)-me*me);    // Momentum of e1 in target system
    Double_t gamma;       // Gamma factor
    //    cout << " g: " << gamma << " s: " << s<< " p: " << p << endl;   
// transform angles into target system
// calculate new momenta and energies 
    Double_t n_theta;
    if (r2->Rndm()<0.5) { // Mott-Streuung
      n_theta = f_mott->GetRandom();
      theta1 = n_theta;
      p1 = p;
      p2 = 0;    
    }
    else {
      n_theta = f_moll->GetRandom();
      // Double_t n_theta = f_mott->GetRandom();
      gamma = (e1->E+2*me)/sqrt(2*me*(2*me+e1->E));
      theta1 = atan2(sin(n_theta),gamma*(cos(n_theta)+1));
      theta2 = atan2(sin(n_theta),gamma*(1-cos(n_theta)));
      p1 = 2*me*(e1->E+2*me)*p*cos(theta1)/(pow((e1->E+2*me),2)-pow(p*cos(theta1),2));
      p2 = 2*me*(e1->E+2*me)*p*cos(theta2)/(pow((e1->E+2*me),2)-pow(p*cos(theta2),2));
    }
    
    e1->E = (sqrt(p1*p1+me*me)-me)-0.5*len/e1->E;
    e2->E = (sqrt(p2*p2+me*me)-me);
    if (e2->E > 0.02) {
      e2->E = e2->E-0.5*len/e2->E;
    }
    else {
      e2->E = 0;
    }

    //    cout << "g: " << gamma << " len: "<< len << " p1: " << p1 << " p2: " << p2 << endl;
    //    cout << "th1: " << theta1 << " th2: " << theta2 << " E1: " << e1->E << " E2: " << e2->E << endl;

// stop if no energy left
    if (e1->E <= E_MIN) {return 0;}
  
// transform into cartesian coordinates (x',y',z') 

    Double_t xn = len * cos(n_phi)*sin(theta1);
    Double_t yn = len * sin(n_phi)*sin(theta1);
    Double_t zn = len * cos(theta1);
    
// Rotation of e1 relative to  previous direction of e1 

    Double_t dx =  xn * cos(ophi)*cos(otheta) - yn * sin(ophi)+ zn* cos(ophi)*sin(otheta);
    Double_t dy =  xn * sin(ophi)*cos(otheta) + yn * cos(ophi)+ zn* sin(ophi)*sin(otheta);
    Double_t dz = -xn * sin(otheta)                           + zn* cos(otheta);
    
// New position and direction of e1

    e1->x += dx;
    e1->y += dy;
    e1->z += dz;
    e1->theta = acos(dz/len);
    e1->phi = atan2(dy,dx);

// Transformation of e2 relative to  previous direction of e1 

    if (p2 > 0) {
      xn = -len * cos(n_phi)*sin(theta2);
      yn = -len * sin(n_phi)*sin(theta2);
      zn =  len * cos(theta2);
      
      dx =  xn * cos(ophi)*cos(otheta) - yn * sin(ophi)+ zn* cos(ophi)*sin(otheta);
      dy =  xn * sin(ophi)*cos(otheta) + yn * cos(ophi)+ zn* sin(ophi)*sin(otheta);
      dz = -xn * sin(otheta)                           + zn* cos(otheta);

// Direction of e2

      e2->theta = acos(dz/len);
      e2->phi   = atan2(dy,dx);
    }

// stop if electron leaves detector
    if ((e1->x < 0) || (e1->x>X_MAX)) {cout << "detector left at x:" << e1->x << endl; return 0;} 
    if ((e1->y < 0) || (e1->y>Y_MAX)) {cout << "detector left at y:" << e1->y << endl; return 0;}

  // return value 1 means success
    return 1;
}

void elektron(void)
{
    ofstream outfile;
    ofstream logfile;
    TList electrons;    // List of electron objects (see root User's guide)
    electron* e1;       // first electron (whose trajectory is followed)
    electron* e2;       // second electron (which is just produced and traced afterwards)
    
// define graph
    TView* view;
    TPolyLine3D* traj = NULL;
    TCanvas* c1 = new TCanvas("SimCanvas", "SimCanvas", 1);
    Int_t k = 0;
    
    // define functions for random number generator
    f_length = new TF1("f_length", "exp(-x)" ,0 ,10);   // mean free path
    f_phi = new TF1("f_phi", "1" ,0 , 2*pi);             // azimuthal angle
    f_moll = new TF1("f_moll",                         // Moeller scattering in c.m. system
		     "pow(3+cos(x),2)/pow(sin(x),4)"
		     ,0.2 ,pi/2);
    f_mott = new TF1("f_mott",
		     "pow(cos(x/2),2)/pow(sin(x/2),4)",0.02,pi);
    // The cross section cannot be integrated to 0 degrees, 
    // a too small starting angle will never produce
    // branches, therefore 0.2 rad is a good compromise
    
    c1->cd();
    view = TView::CreateView(1);
    //    view = new CreateView(1);
    view->SetRange(0,0,0,100,100,200);
    view->ShowAxis();
    
    for (Int_t n = 0; n < N_ELEC; n++) {
	// loop for electrons
	cout << "electron #" << n << endl;
	electrons.Add(new electron(50, 50 ,0 ,E_0, 0, 0));  // push new electron on stack
	while (1) {
	    e1 = (electron*)electrons.First();              // pop next starting point from stack
	    if (e1==NULL) break;
	    electrons.Remove(e1);                           // remove it from the stack  
	    traj = new TPolyLine3D(1024);
	    k = 0;
	    traj->SetPoint(k, e1->x, e1->y, e1->z);
	    traj->Draw();                                                                   
	    k++;
	    while (1) {
		e2 = new electron(0, 0 ,0 ,0 , 0, 0);
		Int_t ret=nextcoord(e1, e2);
		traj->SetPoint(k, e1->x, e1->y, e1->z);
		traj->Draw();
		k++;
		if (ret == 0) break;
		if (e2->E > E_MIN) electrons.Add(e2);     // put secondary electron on the stack
	    }  // end while
      }
      c1->Modified();
      c1->Update();                                                                   
  }  // end for
}
