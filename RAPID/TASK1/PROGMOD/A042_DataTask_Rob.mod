MODULE A042_DataTask_Rob
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

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    CONST num n_A042_PulRatWaiJobRec:=0.01;
    !
    TASK PERS num n_A042_ReadPtrRecBuf:=1;
    !
    CONST num n_A042_NumOfCha:=4;
    TASK PERS num n_A042_ChaNr:=1;
    !
    TASK PERS num n_A042_AccRamp:=33;
    !
    TASK PERS num n_A042_CounterFStr:=0;
    TASK PERS num n_A042_CounterFVal:=0;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    TASK PERS string st_A042_Taskname:="T_ROB1";

    !************************************************
    ! Declaration :     A042_buffer_msg
    !************************************************
    !
    CONST A042_buffer_msg bm_A042_Empty:=[[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE];
    !
    TASK PERS A042_buffer_msg bm_A042_ActSenMsgRob:=[[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE];



ENDMODULE