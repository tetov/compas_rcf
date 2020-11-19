MODULE A042_Base_DataTask_Rob
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A042 Driver
    !
    ! FUNCTION    :  Base Data Task Library  
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.02.20 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2018
    !                - Philippe Fleischmann
    !                - Michael Lyrenmann
    !                - Gonzalo Casas
    !
    ! License     :  You agree that the software source code and documentation
    !                provided by the copyright holder is confidential, 
    !                and you shall take all reasonable precautions to protect
    !                the source code and documentation, and preserve its confidential,
    !                proprietary and trade secret status in perpetuity. 
    ! 
    !                This license is strictly limited to INTERNAL use within one site.
    !
    !***********************************************************************************

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    TASK PERS num n_A042_Answer:=0;
    TASK PERS num n_A042_Act_S_ID:=1;
    TASK PERS num n_A042_Time:=0.5;
    TASK PERS num n_A042_Acc:=100;
    TASK PERS num n_A042_Ramp:=100;
    TASK PERS num n_A042_Override:=100;
    TASK PERS num n_A042_MaxTCP:=500;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    TASK PERS string st_A042_UIAnswer:="Set my Speed";
    TASK PERS string st_A042_ActMsg1:="Requested speed is not posible, minimal value is 0.1 mm/s";
    TASK PERS string st_A042_ActMsg2:="Submited speed : 0.0 mm/s";
    TASK PERS string st_A042_ActMsg3:="";
    TASK PERS string st_A042_ActMsg4:="";
    TASK PERS string st_A042_ActMsg5:="";
    TASK PERS string st_A042_ActBtn1:="50 mm/s";
    TASK PERS string st_A042_ActBtn2:="100 mm/s";
    TASK PERS string st_A042_ActBtn3:="Set my Speed";
    TASK PERS string st_A042_ActBtn4:="";
    TASK PERS string st_A042_ActBtn5:="";
    TASK PERS string st_A042_Header:="Update Speed";
    TASK PERS string st_A042_TPWrite:="18:53 LC 32, 303/626, id 1HH-08-019.";

    !************************************************
    ! Declaration :     tooldata
    !************************************************
    !
    TASK PERS tooldata t_A042_Act:=[TRUE,[[0,0,354],[1,0,0,0]],[5,[10,0,55],[1,0,0,0],0,0,0]];

    !************************************************
    ! Declaration :     wobjdata
    !************************************************
    !
    TASK PERS wobjdata ob_A042_Act:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];

    !************************************************
    ! Declaration :     speeddata
    !************************************************
    !
    CONST speeddata v_A042_Default:=[25,500,5000,1000];
    TASK PERS speeddata v_A042_Act:=[250,500,5000,1000];

    !************************************************
    ! Declaration :     zonedata
    !************************************************
    !
    TASK PERS zonedata z_A042_Act:=[FALSE,150,225,225,23,225,23];

    !************************************************
    ! Declaration :     jointtarget
    !************************************************
    !  
    TASK PERS jointtarget jp_A042_Act:=[[-95,-8,63,0,38,-25],[0,0,0,9E+09,9E+09,9E+09]];

    !************************************************
    ! Declaration :     robtarget
    !************************************************
    !  
    TASK PERS robtarget p_A042_Act:=[[1324.24,-911.562,-124.193],[-0.0133653,0.177374,0.981452,-0.0714921],[0,0,1,0],[0,0,0,9E+09,9E+09,9E+09]];

    !************************************************
    ! Declaration :     signaldo
    !************************************************
    !
    VAR signaldo do_A042_Act;

    !************************************************
    ! Declaration :     signalgo
    !************************************************
    !
    VAR signalgo go_A042_Act;

    !************************************************
    ! Declaration :     signalao
    !************************************************
    !
    VAR signalao ao_A042_Act;

    !************************************************
    ! Declaration :     signaldi
    !************************************************
    !
    VAR signaldi di_A042_Act;

    !************************************************
    ! Declaration :     signalgi
    !************************************************
    !
    VAR signalgi gi_A042_Act;

    !************************************************
    ! Declaration :     signalai
    !************************************************
    !
    VAR signalai ai_A042_Act;

    !************************************************
    ! Declaration :     signalai
    !************************************************
    !
    VAR clock ck_A042_StopWatch;

ENDMODULE