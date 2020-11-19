MODULE A042_DataGlobal
    !***********************************************************************************
    !
    ! ETH Zurich / Robotic Fabrication Lab
    ! HIB C13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A042 Driver
    !
    ! FUNCTION    :  Inclouds all project spezific global datas 
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
    PERS bool b_A042_TaskReceiverOn;
    PERS bool b_A042_TaskSenderOn;
    !
    PERS bool b_A042_MaWaitForJob;
    PERS bool b_A042_MaHamModOn;
    PERS bool b_A042_MaInUse;
    PERS bool b_A042_AutoIPAddress;
    PERS bool b_A042_VirtualCustomPorts;
    !
    ! Channels
    PERS bool b_A042_Com{n_A042_NumOfCha};
    PERS bool b_A042_SIDCheck{n_A042_NumOfCha};
    PERS bool b_A042_SIDErrorStop{n_A042_NumOfCha};
    PERS bool b_A042_LogPro{n_A042_NumOfCha};
    !
    ! Client information
    PERS bool b_A042_PPMain;
    !
    ! Activate or deactivate a event log message 
    PERS bool b_A042_EvLogReadAndUnpackTime;
    PERS bool b_A042_EvLogPackAndSendTime;
    PERS bool b_A042_EvLogMsgInUntilMsgOutTime;
    !
    ! Temporary to measure the feedback loop
    PERS bool b_A042_FeedbackOut;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    PERS num n_A042_WritePtrSenBufMa{n_A042_NumOfCha};
    PERS num n_A042_WritePtrSenBufRob{n_A042_NumOfCha};
    PERS num n_A042_SIDMax;
    !
    PERS num n_A042_R1_ChaNr;
    PERS num n_A042_R2_ChaNr;
    PERS num n_A042_R3_ChaNr;
    PERS num n_A042_R4_ChaNr;
    !
    PERS num n_A042_SocketPortRec{n_A042_NumOfCha};
    PERS num n_A042_SocketPortSen{n_A042_NumOfCha};
    !
    PERS num n_A042_TimeTaskLiAll;
    PERS num n_A042_TimeTPMsg;
    !
    PERS num n_A042_ProtocolVersion;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    PERS string n_A042_Version;
    !
    PERS string st_A042_JobForMa;
    !
    PERS string st_A042_IP_Address;
    PERS string st_A042_IP_AddressVC;
    PERS string st_A042_IP_AddressMan;
    !
    ! System data 
    PERS string st_A042_SerialNr;
    PERS string st_A042_SoftwareVersion;
    PERS string st_A042_RobotWare;
    PERS string st_A042_ControllerID;
    PERS string st_A042_WAN_IP;
    PERS string st_A042_ControllerLang;
    PERS string st_A042_SystemName;

    !************************************************
    ! Declaration :     tasklist
    !************************************************
    !
    !PERS tasks tl_A042_All{5};
    PERS tasks tl_A042_All{7};

    !************************************************
    ! Declaration :     syncident
    !************************************************
    !
    VAR syncident id_A042_MainSta;
    VAR syncident id_A042_MainEnd;
    !
    VAR syncident id_A042_InitSta;
    VAR syncident id_A042_InitMa;
    VAR syncident id_A042_InitEnd;

    !************************************************
    ! Declaration :     A042_channel
    !************************************************
    !
    PERS A042_channel ch_A042_Channels;

    !************************************************
    ! Declaration :     buffer_msg
    !************************************************
    !
    ! Receiver buffer for master
    PERS A042_buffer_msg bm_A042_RecBufferMa{n_A042_NumOfCha,10};
    !
    ! Receiver buffer for robots
    PERS A042_buffer_msg bm_A042_RecBufferRob{n_A042_NumOfCha,10};
    !
    ! Sender buffer for master
    PERS A042_buffer_msg bm_A042_SenBufferMa{n_A042_NumOfCha,10};
    !
    ! Sender buffer for robots
    PERS A042_buffer_msg bm_A042_SenBufferRob{n_A042_NumOfCha,10};

ENDMODULE