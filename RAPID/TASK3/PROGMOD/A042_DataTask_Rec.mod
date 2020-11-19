MODULE A042_DataTask_Rec
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
    TASK PERS bool b_A042_SocketActiv:=TRUE;
    TASK PERS bool b_A042_PrintPrio1:=FALSE;
    TASK PERS bool b_A042_PrintPrio2:=FALSE;
    !
    TASK PERS bool b_A042_BufFullMa{n_A042_NumOfCha}:=[FALSE,FALSE,FALSE,FALSE];
    TASK PERS bool b_A042_BufFullRob{n_A042_NumOfCha}:=[TRUE,FALSE,FALSE,FALSE];
    TASK PERS bool b_A042_LogHelper{n_A042_NumOfCha}:=[FALSE,FALSE,FALSE,FALSE];
    !
    TASK PERS bool b_A042_FirstProtocolAfterPPMain:=FALSE;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    CONST num n_A042_NumOfCha:=4;
    CONST num n_A042_RecMinData:=49;
    CONST num n_A042_NoOfByMsgLen:=4;
    CONST num n_A042_TimeOutRecRobSocRec:=10;
    !
    TASK PERS num n_A042_WritePtrBufMa{n_A042_NumOfCha}:=[0,0,0,0];
    TASK PERS num n_A042_WritePtrBufRob{n_A042_NumOfCha}:=[6,0,0,0];
    TASK PERS num n_A042_SIDExpected{n_A042_NumOfCha}:=[2857,0,0,0];
    TASK PERS num n_A042_SIDIs{n_A042_NumOfCha}:=[70001,0,0,0];
    !
    VAR num n_A042_MsgLenRob{n_A042_NumOfCha};
    VAR num n_A042_NoOfRecBytesRob{n_A042_NumOfCha};

    !************************************************
    ! Declaration :     string
    !************************************************
    !  
    TASK PERS string st_A042_EvLogMsgHeader:="A042 -- Receiver";
    !
    TASK PERS string st_A042_UIAnswer:="Stop";
    TASK PERS string st_A042_ActMsg1:="Expected protocol version: 2.0";
    TASK PERS string st_A042_ActMsg2:="Received protocol version: 4.0";
    TASK PERS string st_A042_ActMsg3:="Expected: 2";
    TASK PERS string st_A042_ActMsg4:="Received: 70001";
    TASK PERS string st_A042_ActMsg5:="";
    TASK PERS string st_A042_ActBtn1:="Stop";
    TASK PERS string st_A042_ActBtn2:="100 mm/s";
    TASK PERS string st_A042_ActBtn3:="Set my Speed";
    TASK PERS string st_A042_ActBtn4:="";
    TASK PERS string st_A042_ActBtn5:="";
    TASK PERS string st_A042_Header:="Protocol mismatch";
    !  
    VAR string st_A042_IP_ClientRec{n_A042_NumOfCha}:=["","","",""];

    !************************************************
    ! Declaration :     clock
    !************************************************
    !
    VAR clock clk_A042_ReadAndUnpack;
    VAR clock clk_A042_MsgInUntilMsgOut;

    !************************************************
    ! Declaration :     A042_Protokol
    !************************************************
    !
    CONST A042_Protocol pro_A042_Empty:=[[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]];
    !
    VAR A042_Protocol pro_A042_ActMsgRob:=[[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]];
    !
    TASK PERS A042_Protocol pro_A042_ActMsgTemp:=[[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]];
    !
    TASK PERS A042_Protocol pro_A042_ActMsgRec{n_A042_NumOfCha}:=[
    [[120,2,1.60493E+09,191],[2857,0,12,"r_A042_MoveJ",0,0,"",0,0,5,"wobj0",0,"",0,"",0,"",0,"",0,"",0,"",0,"",15,-1350.92,-733.563,226.92,-0.000916494,0.70506,0.70913,0.00485062,0,0,0,0,0,0,120,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[67,4,1.58281E+09,242],[4,0,15,"r_A042_WaitTime",1,0,"",0,0,24,"E-Level Channel 2 Master",0,"",0,"",0,"",0,"",0,"",0,"",0,"",1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[120,4,1.55775E+09,695],[11,0,12,"r_A042_MoveL",1,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",15,542.04,-200,237.57,0,0,1,0,28000,-3400,-3138,0,0,0,230,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[120,4,1.55775E+09,695],[11,0,12,"r_A042_MoveL",1,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",15,542.04,-200,237.57,0,0,1,0,28000,-3400,-3138,0,0,0,230,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]];

    !************************************************
    ! Declaration :     rawbytes
    !************************************************
    !
    VAR rawbytes rb_A042_BufferMsgLenRob{n_A042_NumOfCha};
    VAR rawbytes rb_A042_BufferRob{n_A042_NumOfCha};

    !************************************************
    ! Declaration :     socketdev
    !************************************************
    !  
    VAR socketdev sod_A042_ServerRec{n_A042_NumOfCha};
    VAR socketdev sod_A042_ClientRec{n_A042_NumOfCha};

    !************************************************
    ! Declaration :     A042_buffer_msg
    !************************************************
    !
    CONST A042_buffer_msg bmEmpty:=[[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE];
ENDMODULE