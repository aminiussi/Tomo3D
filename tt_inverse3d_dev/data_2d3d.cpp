#include <iostream>
#include <fstream>
#include <cstdio>
#include "data_2d3d.hpp"

using namespace std;

data_2d3d :: data_2d3d(int nn, int nzz, std::string const& input2D, std::string const& input3D) {

	nx=1;
	ny=nn;
	nz=nzz;
	dif=0.;
	plane=1;
	ns=0,npicks=0,raycode=0;
	vw=0,va=0,tt=0,dt=0;
	ss=0,sZ=0,rr=0,rZ=0;
	ref=0,depth=0;
	char_xy=0;

        num=0,num0=0;num2=2;
        xmin=0,xmax=1;
        ymin=0,ymax=1;
        zmin=0,zmax=1;
        lx_top=1,lx_bot=1;
        ly_top=1,ly_bot=1;
        lz_top=1,lz_bot=1;
        lxr=0,lyr=0;

	//apertura de archivos
        file.open(input2D);
        file3D.open(input3D);

}

data_2d3d :: ~data_2d3d() {

	//cierre de archivos
	file.close();
	file3D.close();

}

void data_2d3d :: meshfn_2d3d() {

// INPUT MODELO DE VELOCIDAD

	file >> ny >> nz >> vw >> va;

// Asignacion memoria dinamica

	double* posX = new double [nx];
	double* posY = new double [ny];
	double* bat = new double [ny];
	double* posZ = new double [nz];
	double** vel = new double* [ny];
	for(int j=0;j<ny;j++) {
		vel[j]=new double[nz];
	}

// Lectura de archivo input 2D

	for(int j=0;j<ny;j++) {
		file >> posY[j];
	}

	for(int j=0;j<ny;j++) {
		file >> bat[j];
	}

	for(int k=0;k<nz;k++) {
		file >> posZ[k];
	}

	for (int j = 0; j < ny; j++){
		for (int k = 0; k < nz; k++) {
			file >> vel[j][k];
		}
	}

// Escritura archivo 3D

// Primera fila
	file3D << nx << '\t' << ny << '\t' << nz << '\t' << vw << '\t' << va << '\n';

// Segunda fila: posX
	file3D << plane  << '\n';

// Tercera fila: posY
	for(int j=0;j<ny;j++) {
		file3D << posY[j] << '\t';
	}
	file3D << '\n';

// Cuarto bloque: batimetria
	for(int j=0;j<ny;j++) {
		file3D << bat[j] << '\t';
	}
	file3D << '\n';

// Quinta fila: posZ
	for(int k=0;k<nz;k++) {
		file3D << posZ[k] << '\t';
	}
	file3D << '\n';

// Sexto bloque: velocidad
	for(int j=0;j<ny;j++) {
		for(int k=0;k<nz;k++) {
			file3D << vel[j][k] << '\t';
		}
		file3D << '\n';
	}

// Designacion de memoria dinamica

	delete[] posX;
	delete[] posY;
	delete[] bat;
	delete[] posZ;
	for(int j = 0; j < ny; j++) {
	delete[] vel[j];
	}
	delete[] vel;

}

void data_2d3d :: datafn_2d3d() {

	// INPUT WAS TRAVEL TIMES

	file >> ns;
	file3D << ns << '\n';

	for(int i=0;i<ns;i++) {
		file >> char_xy >> ss >> sZ >> npicks;
		file3D << 's' << '\t' << plane << '\t' << ss << '\t' << sZ << '\t' << npicks << '\t' << '\n';
		for(int j=0;j<npicks;j++) {
			file >> char_xy >> rr >> rZ >> raycode >> tt >> dt;
			file3D << 'r' << '\t' << plane << '\t' << rr << '\t' << rZ << '\t' << raycode << '\t' << tt << '\t' << dt << '\n';
		}
	}

}


void data_2d3d :: reflfn_2d3d() {

	// INPUT REFLECTOR

	file3D << nx << '\t' << ny << '\n';

	for(int j=0;j<ny;j++) {

		file >> ref >> depth;
		file3D << plane << '\t' << ref << '\t' << depth << '\n';

	}

}

void data_2d3d :: corr_velfn_2d3d() {

        file >> num >> num;
        file >> ymin >> ymax;
        file >> num >> num;
        file >> zmin >> zmax;
        file >> ly_top >> ly_bot;
        file >> ly_top >> ly_bot;
        file >> lz_top >> lz_bot;
        file >> lz_top >> lz_bot;

        file3D << num2 << '\t' << num2 << '\t' << num2;
        file3D << '\n';
        file3D << xmin << '\t' << xmax;
        file3D << '\n';
        file3D << ymin << '\t' << ymax;
        file3D << '\n';
        file3D << num0 << '\t' << num0;
        file3D << '\n';
        file3D << num0 << '\t' << num0;
        file3D << '\n';
        file3D << zmin << '\t' << zmax;
        file3D << '\n';
        file3D << lx_top << '\t' << lx_bot;
        file3D << '\n';
        file3D << lx_top << '\t' << lx_bot;
        file3D << '\n';
        file3D << lx_top << '\t' << lx_bot;
        file3D << '\n';
        file3D << lx_top << '\t' << lx_bot;
        file3D << '\n';
        file3D << ly_top << '\t' << ly_bot;
        file3D << '\n';
        file3D << ly_top << '\t' << ly_bot;
        file3D << '\n';
        file3D << ly_top << '\t' << ly_bot;
        file3D << '\n';
        file3D << ly_top << '\t' << ly_bot;
        file3D << '\n';
        file3D << lz_top << '\t' << lz_bot;
        file3D << '\n';
        file3D << lz_top << '\t' << lz_bot;
        file3D << '\n';
        file3D << lz_top << '\t' << lz_bot;
        file3D << '\n';
        file3D << lz_top << '\t' << lz_bot;

}

void data_2d3d :: corr_depfn_2d3d() {

	file >> ymin >> lyr;
	file >> ymax >> lyr;

	file3D << num2 << '\t' << num2;
	file3D << '\n';

	file3D << xmin << '\t'<< ymin << '\t' << lxr << '\t' << lyr;
	file3D << '\n';

	file3D << xmin << '\t'<< ymax << '\t' << lxr << '\t' << lyr;
	file3D << '\n';

	file3D << xmax << '\t' << ymin << '\t' << lxr << '\t' <<lyr;
	file3D << '\n';

	file3D << xmax << '\t' << ymax << '\t' << lxr << '\t' << lyr;

}
