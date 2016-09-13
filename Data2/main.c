#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <math.h>

#include "../CHARGE/charge.h"
//#include "../MEM/mem.h"
#include "../FUNCTIONS/functions.h"
#include "../PARAMETERS/read.h"
#include "../CHARGETRANSPORT/chargetransport.h"
#include "../CLUSTER/CLUSTERFUNCTIONS/clusterfunctions.h"
#include "../CLUSTER/CLUSTERSITENODE/clustersitenode.h"
#include "../CLUSTER/CLUSTERFUNCTIONS/SITENODE/sitenode.h"
#include "../CLUSTER/CLUSTERFUNCTIONS/MATRIX/matrix.h"
#include "../CLUSTER/CLUSTERFUNCTIONS/DATASTRUCT/cluster.h"
#include "../IO/io.h"

int main(void){

	//Program Timer
	time_t start;
	time_t finish;
	
	clock_t begin;
	clock_t end;
	double time_spent;
	begin = clock();
	time(&start);

	srand(time(NULL));

	//mem_init();
	
	//Constants
	//Boltzmann constant Units of [eV/K]
	//static const double kB = 8.6173324E-5;

	//Variables from ParameterFrame
	int method;
	int SLength;
	int SWidth;
	int SHeight;
	double VoltageX;
	double VoltageY;
	double VoltageZ;
	int VStepX;
	int VStepY;
	int VStepZ;
	double VincX;
	double VincY;
	double VincZ;
	double SiteDistance;
	int Rcount;
	double TempStart;
	int TemperatureStep;
	double TemperatureInc;
	int r;
	double Vx;
	double Vy;
	double Vz;
	//double KT;
	double Temperature;

	//Local Variables
	int CheckPtStatus;
	int CheckFileExist;
	int CheckPointNum;
	int count;
	//int OrderL;
	double electricFieldX;
	double electricFieldY;
	double electricFieldZ;
	double electricEnergyX;
	double electricEnergyY;
	double electricEnergyZ;
	int Vxcount;
	int Vycount;
	int Vzcount;
	
	Electrode elXb = NULL;
	Electrode elXf = NULL;
	Electrode elYl = NULL;
	Electrode elYr = NULL;
	Electrode elZb = NULL;
	Electrode elZa = NULL;

	//Variables needed by RandomWalk
	int FileNameSize;
	long int n;
	int nc;
	int nca;
	long double t;
	matrix Sequence;
	matrix FutureSite;
	SNarray snA;
	ArbArray ClArLL = NULL;
	ChargeArray chA;
	ParameterFrame PF;
	
	FileNameSize = 256;

	char FileName[FileNameSize];
	char FileNameCheckPt[FileNameSize];
	char FileNameCheckPtVersion[FileNameSize];

	n = 0;
	nc = 0;
	nca = 0;
	t = 0;
	//KT = 0;

	PF = NULL;
	FileName[0] = '\0';
	FileNameCheckPt[0] = '\0';
	FileNameCheckPtVersion[0] = '\0';

	//Check first to see if a CheckPoint file exists 
	//in the CheckPoint folder return -1 if no .ckpt file or other problems
	CheckFileExist = CheckPt_exist(FileNameCheckPt,FileNameSize);
	printf("Value of CheckFileExist %d\n",CheckFileExist);
	if(CheckFileExist == 0){
		//This means a Checkpoint file does exist 
		printf("Loading Parameter Frame from checkpoint file\n");
		Load_CheckPt_PF(FileNameCheckPt, &PF);
	}else{
		//This means a checkpoint file does not exist
		//Starting from scratch reading from parameterfile
		PF = newParamFrame_File();
		printf("Loading Parameter Frame from parameter.txt file\n");
	}

	//Initializing ParameterFrame Variables
	method = PFget_method(PF);
	SLength = PFget_Len(PF);
	SWidth = PFget_Wid(PF);
	SHeight = PFget_Hei(PF);
	VoltageX = PFget_VoltageX(PF);
	VoltageY = PFget_VoltageY(PF);
	VoltageZ = PFget_VoltageZ(PF);
	VStepX = PFget_VStepX(PF);
	VStepY = PFget_VStepY(PF);
	VStepZ = PFget_VStepZ(PF);
	VincX = PFget_VincX(PF);
	VincY = PFget_VincY(PF);
	VincZ = PFget_VincZ(PF);
	SiteDistance = PFget_SiteDist(PF);
	Rcount = PFget_Rcount(PF);
	TempStart = PFget_TempStart(PF);
	TemperatureStep = PFget_TempStep(PF);
	TemperatureInc = PFget_TempInc(PF);

	Vx = VoltageX;
	Vy = VoltageY;
	Vz = VoltageZ;

	Vxcount = 0;

	//TOF method
	if(method==0){
		//Cycle through Xvoltages
		//	mem_check();
		while(Vxcount<=VStepX){
			Vy = VoltageY;
			Vycount = 0;

			//Cycle through Yvoltages
			while(Vycount<=VStepY){
				Vz = VoltageZ;
				Vzcount = 0;

				//Cycle through Zvoltages
				while(Vzcount<=VStepZ){

					for(count=0;count<TemperatureStep;count++){

						Temperature = TempStart;
						//KT = kB*Temperature; 

						for(r=1;r<Rcount+1;r++){

							//Electric field from voltage
							electricFieldX = Vx / (SLength*SiteDistance);
							electricFieldY = Vy / (SWidth*SiteDistance);
							electricFieldZ = Vz / (SHeight*SiteDistance);

							//Electrical energy from voltage between two sites
							electricEnergyX = SiteDistance*electricFieldX;
							electricEnergyY = SiteDistance*electricFieldY;
							electricEnergyZ = SiteDistance*electricFieldZ;

							printf("Calculating .ckpt status\n");
							CheckPtStatus = -1;
							CheckPtStatus = CheckPt_Test_TOF(&CheckPointNum, CheckFileExist, FileNameCheckPtVersion,\
									FileNameSize,Vx, Vy, Vz, Temperature);

							sprintf(FileName,"DataT%gVx%gVy%gVz%gR%d",Temperature,Vx,Vy,Vz,r);

							Pre_randomWalk(CheckPtStatus, FileNameCheckPtVersion,FileName, &t, &Sequence, &chA,\
									&FutureSite,&ClArLL, &snA, PF,\
									electricEnergyX, electricEnergyY, electricEnergyZ,r,Vx,Vy,Vz, Temperature,\
									&n, &nc, &nca, &elXb, &elXf, &elYl, &elYr, &elZb, &elZa);	

							if(FutureSite==NULL){
								printf("FutureSite matrix NULL\n");
								exit(1);
							}

							printFileEnergy(snA, &FileName[0],electricEnergyX, electricEnergyY, electricEnergyZ, PF);
							printMatrix(FutureSite);

							randomWalk(snA, CheckPointNum, &FileName[0],\
									electricFieldX,	electricFieldY, electricFieldZ,\
									elXb, elXf, elYl, elYr, elZb, elZa, PF, t, Sequence,\
									FutureSite, &chA, n, nc, nca, Temperature); 

							printf("Printing Visit Freq files\n");
							printVisitFreq(snA,&FileName[0]);

							Post_randomWalk(ClArLL, snA, elXb, elXf, elYl, elYr, elZb, elZa,PF);

						}

						Temperature += TemperatureInc;
					}
					Vzcount++;
					Vz += VincZ;
				}
				Vycount++;
				Vy += VincY;
			}
			Vxcount++;
			Vx += VincX;
		}
	}else if(method==1){
		//CELIV method
		for(count=0;count<TemperatureStep;count++){

			Temperature = TempStart;
			//KT = kB*Temperature; 

			for(r=1;r<Rcount+1;r++){

				//Electric field from voltage
				electricFieldX = Vx / (SLength*SiteDistance);
				electricFieldY = Vy / (SWidth*SiteDistance);
				electricFieldZ = Vz / (SHeight*SiteDistance);

				//Electrical energy from voltage between two sites
				electricEnergyX = SiteDistance*electricFieldX;
				electricEnergyY = SiteDistance*electricFieldY;
				electricEnergyZ = SiteDistance*electricFieldZ;

				printf("Calculating .ckpt status\n");
				CheckPtStatus = -1;
				CheckPtStatus = CheckPt_Test_CELIV( &CheckPointNum, CheckFileExist, FileNameCheckPtVersion,\
						FileNameSize,Temperature);

				sprintf(FileName,"DataT%gR%d",Temperature,r);

				Pre_randomWalk(CheckPtStatus, FileNameCheckPtVersion,FileName, &t, &Sequence, &chA,\
						&FutureSite,&ClArLL, &snA, PF,\
						electricEnergyX, electricEnergyY, electricEnergyZ,r,Vx,Vy,Vz, Temperature,\
						&n, &nc, &nca, &elXb, &elXf, &elYl, &elYr, &elZb, &elZa);	

				if(FutureSite==NULL){
					printf("FutureSite matrix NULL\n");
					exit(1);
				}

				randomWalk(snA, CheckPointNum, &FileName[0],\
						electricFieldX,	electricFieldY, electricFieldZ,\
						elXb, elXf, elYl, elYr, elZb, elZa, PF, t, Sequence,\
						FutureSite, &chA, n, nc, nca, Temperature); 

				printf("Printing Visit Freq files\n");
				printVisitFreq(snA,&FileName[0]);

				Post_randomWalk(ClArLL, snA, elXb, elXf, elYl, elYr, elZb, elZa,PF);

			}

			Temperature += TemperatureInc;
		}

	}else{
		printf("ERROR method option can only be ToF (method==0) or CELIV (method==1)\n");
	}
	end = clock();
	time_spent = (double)(end-begin) / CLOCKS_PER_SEC;
	time(&finish);
	//second = CPU_TIME;
	printf("Run Time %g seconds\n",time_spent);
	//printf("cpu : %.2f secs\n", second-first);
	printf("user : %d secs\n", (int)(finish-start));

	//FILE * LogFile;

	if(PFget_LogFile(PF)==1){
		//LogFile = appendLogFile(FileName);			
		LogFile_printTime(FileName, time_spent, (int)(finish-start));
		//closeLogFile(LogFile);
	}
	
	deleteParamFrame(&PF);

	//atexit(mem_term);

	return 0;
}
