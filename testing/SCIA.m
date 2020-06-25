close all 
clear all
clearvars
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Enter parameter %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
path = 'C:\Users\279295C\Documents\postdoc_1\SCIA';
cd 'C:\Users\279295C\Documents\postdoc_1\SCIA';

area=readtable('area.csv');
area_size =area(:,13);
area_size=table2array(area_size);
area_size=6989.802;
ID=area(:,7);
ID=table2array(ID);
%%%%

extension='txt';
filelist = dir([path,'/*',extension]);
file_name=struct2table(filelist);
file_name=(file_name(:,1));
file_name=table2array(file_name);
file_name=char(file_name);
nfiles = length(filelist);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Enter parameter %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
area_real_100=area_size(1,1);
thiessen_real=readtable('thiessen_id_206.txt');


area_pol=thiessen_real(:,20);
area_pol=table2array(area_pol);
n_craters=size(area_pol);
n_craters=n_craters(1,1);
max_bin=mean(area_pol)*4;
nbins_real=min(area_pol):median(area_pol)/10:max(area_pol);
max_plot=median(area_pol)*10;

edge=sqrt(area_real_100);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% iteration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

n_it=100;


SIMU=[];

for k=1:n_it;
    edge=sqrt(area_real_100);
    x = 0 + (edge-0).*rand(n_craters,1);
    y = 0 + (edge-0).*rand(n_craters,1);
    figure(1)
    subplot(2,2,2)
    voronoi(x,y);
    figure(2)
    sdata=[x,y];
    [ v, c] = voronoin ( sdata );
    tess_area_rand=zeros(size(c,1),1);
    for i = 1 : size(c ,1);
        ind = c{i}';
        if ind~=1;
            tess_area_rand(i,1) = polyarea( v(ind,1) , v(ind,2) );
        end
    end
    tess_area_rand(tess_area_rand==0 ) = [];
    max_plot=median(tess_area_rand)*10;
    nbins_sim=nbins_real;
    f=hist(tess_area_rand,nbins_sim);
    plot(nbins_sim,f,'Color',[0.7 0.7 0.7]);

    xlim([0 max_plot]);
    hold on
    
    for n=n_it;
        SIMU=[SIMU f(:)];        
    end
end
hold on

SIMU=SIMU';

p1=plot(nbins_sim,f,'Color',[0.7 0.7 0.7]);

f_real=hist(area_pol,nbins_sim);
f_real=smooth(f_real);
p2=plot(nbins_sim,f_real,'LineWidth',2,'Color', [1 0 0]);

mean_simu=mean(SIMU);
std_simu_pos=mean_simu+(std(SIMU));
std_simu_neg=mean_simu-(std(SIMU));

hold on
p3=plot(nbins_sim,mean_simu,'LineWidth',2,'Color',[0 1 0]);
hold on
p4=plot(nbins_sim,std_simu_pos,'LineStyle','--','LineWidth',1,'Color',[0 1 0]);
hold on
plot(nbins_sim,std_simu_neg,'LineStyle','--','LineWidth',1,'Color',[0 1 0]);




std_simu_pos_trans=std_simu_pos';
sample=0:0.0001:max_plot;
f_real_interp=interp1(nbins_sim(1:end),f_real(1:end),sample);
std_simu_pos_trans_interp=interp1(nbins_sim(1:end),std_simu_pos_trans(1:end),sample);

eps=0.5;
idx = find(abs(f_real_interp - std_simu_pos_trans_interp) < eps, 2);
px = sample(idx(1,2));
py = f_real_interp(idx(1,2));
hold on
plot(px, py, 'ro', 'MarkerSize', 18,'Color',[0 0 0]);
hold on 
threshold_line=plot([px px],[0 py],'k');


max_y_plot=max(mean_simu)+40;

ylim([0 max_y_plot]);
xlabel('Voronoi polygon area')
ylabel('Number of polygons')
% title('comp')
legend([p2,p1,p3,p4],'Data','Random data','Mean of random data','1\sigma confidence envelope')

Threshold_area=px

secondary=find(area_pol<Threshold_area);
s=size(secondary);
nb_secondary=s(1,1)
percent_crat_rm=(nb_secondary/n_craters)*100

formatspace='Threshold area = %d';
str=sprintf(formatspace,Threshold_area);
annotation('textbox',[.3 .5 .1 .1],'string',str)

formatspace='Percent of secondary craters = %d';
str=sprintf(formatspace,percent_crat_rm);
annotation('textbox',[.3 .4 .1 .1],'string',str)

formatspace='Number of secondary craters = %d';
str=sprintf(formatspace,nb_secondary);
annotation('textbox',[.3 .3 .1 .1],'string',str)
