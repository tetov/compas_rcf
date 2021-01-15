MODULE A042_DataTask_Sen
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
    TASK PERS bool b_A042_PrintPrio1:=FALSE;
    !
    TASK PERS bool b_A042_SocketActiv:=TRUE;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    CONST num n_A042_NumOfCha:=4;
    CONST num n_A042_SenMinData:=1;
    CONST num n_A042_NoOfByMsgLen:=4;
    CONST num n_A042_SenHeaderMaxSqzNrRob:=1000000;
    CONST num n_A042_ProtocolMa:=1;
    CONST num n_A042_ProtocolRob:=2;
    CONST num n_A042_SendProtocolPerChannel:=2;
    !
    TASK PERS num n_A042_ReadPtrSenBufRob{n_A042_NumOfCha}:=[6,1,1,1];
    TASK PERS num n_A042_ReadPtrSenBufMa{n_A042_NumOfCha}:=[1,1,1,1];
    !
    TASK PERS num n_A042_SenHeaderSqzNr{n_A042_NumOfCha}:=[5,0,0,0];
    !
    TASK PERS num n_A042_SenMsgLenRob:=68;
    !
    TASK PERS num n_A042_TimeStamp:=123.591;
    TASK PERS num n_A042_TimeStampSec:=123;
    TASK PERS num n_A042_TimeStampNanoSec:=591;


    !************************************************
    ! Declaration :     string
    !************************************************
    !
    TASK PERS string st_A042_EvLogMsgHeader:="A042 -- Sender";
    !  
    VAR string st_A042_IP_ClientSen{n_A042_NumOfCha}:=["","","",""];

    !************************************************
    ! Declaration :     clock
    !************************************************
    !
    VAR clock clk_A042_TimeStamp;
    VAR clock clk_A042_PackAndSend;

    !************************************************
    ! Declaration :     socketdev
    !************************************************
    !  
    TASK VAR socketdev sod_A042_ServerSen{n_A042_NumOfCha};
    TASK VAR socketdev sod_A042_ClientSen{n_A042_NumOfCha};

    !************************************************
    ! Declaration :     A042_Protokol
    !************************************************
    !
    CONST A042_Protocol proEmpty:=[[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]];
    !
    !* TASK VAR A042_Protocol pro_A042_ActMsgRob:=[[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]];
    !
    TASK PERS A042_Protocol pro_A042_ActMsgSen{n_A042_SendProtocolPerChannel,n_A042_NumOfCha}:=[
    [[[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]],

    [[[72,2,123,591],[5,0,16,"r_A042_WatchRead",0,4,"Done",96,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",1,26.301,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0],[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]]];

    !************************************************
    ! Declaration :     rawbytes
    !************************************************
    !
    TASK VAR rawbytes rb_A042_SenTempBuffer;
    TASK VAR rawbytes rb_A042_SenBufferMsgLen;
    TASK VAR rawbytes rb_A042_SenBuffer;

    !************************************************
    ! Declaration :     A042_buffer_msg
    !************************************************
    !
    CONST A042_buffer_msg bmEmpty:=[[0,0,0,"",0,0,"",0,0,0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,"",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],FALSE];

ENDMODULE