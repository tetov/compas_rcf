MODULE A042_DataTask_Ma
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
    ! FUNCTION    :  Includ all Task specific Data's
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2018.06.17 Draft
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
    ! Declaration :     bool
    !************************************************
    !
    CONST bool b_A042_Run:=TRUE;
    !
    TASK PERS bool b_A042_CyclicJob{n_A042_NumOfCha}:=[FALSE,FALSE,FALSE,FALSE];
    TASK PERS bool b_A042_CycleTimeRunnig{n_A042_NumOfCha}:=[FALSE,FALSE,FALSE,FALSE];

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    CONST num n_A042_NumOfCha:=4;
    !
    CONST num n_A042_DefaultSocketPortRec{n_A042_NumOfCha}:=[30101,30102,30103,30104];
    CONST num n_A042_DefaultSocketPortSen{n_A042_NumOfCha}:=[30201,30202,30203,30204];
    !
    TASK PERS num n_A042_ViCustomSocketPortRec{n_A042_NumOfCha}:=[31101,31102,31103,31104];
    TASK PERS num n_A042_ViCustomSocketPortSen{n_A042_NumOfCha}:=[31201,31202,31203,31204];
    !
    TASK PERS num n_A042_ChaNr:=1;
    TASK PERS num n_A042_ReadPtrRecBuf{n_A042_NumOfCha}:=[1,1,1,1];
    TASK PERS num n_A042_Act_S_ID:=1;
    TASK PERS num n_A042_CounterFStr{n_A042_NumOfCha}:=[0,0,0,0];
    TASK PERS num n_A042_CounterFVal{n_A042_NumOfCha}:=[0,0,0,0];
    TASK PERS num n_A042_CyJobStart_S_ID{n_A042_NumOfCha}:=[1,0,0,0];
    TASK PERS num n_A042_MinCycleTime{n_A042_NumOfCha}:=[1,1,1,1];
    TASK PERS num n_A042_ActCycleTime{n_A042_NumOfCha}:=[0.364,1,1,1];
    TASK PERS num n_A042_LastCycleTime{n_A042_NumOfCha}:=[1.001,1,1,1];
    TASK PERS num n_A042_ActCycle{n_A042_NumOfCha}:=[55.002,1,1,1];

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    TASK PERS string st_A042_ChaTask:="T_ROB1";
    TASK PERS string st_A042_EvLogMsgHeader:="A042 -- Master";
    !
    TASK PERS string st_A042_CyclicJob{n_A042_NumOfCha}:=["r_A042_GetJointT","","",""];
    TASK PERS string st_A042_TPWrite{n_A042_NumOfCha}:=["E-Level Channel 1 Master","E-Level Channel 2 Master","",""];

    !************************************************
    ! Declaration :     jointtarget
    !************************************************
    !  
    TASK PERS jointtarget jp_A042_Act:=[[0,0,0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    !************************************************
    ! Declaration :     robtarget
    !************************************************
    !  
    TASK PERS robtarget p_A042_Act:=[[10270.7,5902.7,955.503],[0.33371,0.672327,0.217398,-0.623981],[1,1,-1,1],[8000,-4200,-2500,0,0,0]];

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    VAR clock ck_A042_CycleJob{n_A042_NumOfCha};

    !************************************************
    ! Declaration :     A042_buffer_msg
    !************************************************
    !
    CONST A042_buffer_msg bm_A042_Empty:=[[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE];
    !
    TASK PERS A042_buffer_msg bm_A042_ActSenMsgMa{n_A042_NumOfCha}:=[
    [[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE],
    [[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE],
    [[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE],
    [[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE]];

ENDMODULE