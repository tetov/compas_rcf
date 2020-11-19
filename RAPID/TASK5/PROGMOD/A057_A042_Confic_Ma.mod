MODULE A057_A042_Confic_Ma
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
    ! FUNCTION    :  Configuration modul for the project 
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.05.06 Draft
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
    ! Function    :     Initialize Cell
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.06.28
    ! **************** ETH Zürich *******************
    !
    PROC r_A057_A042_Config()
        !
        ! Tasklists 
        tl_A042_All:=[["T_MASTER"],["RECEIVER"],["SENDER"],["T_ROB1"],[""],[""],[""]];
        !
        ! Channel 1
        ch_A042_Channels.Ch_1.T_Name:="T_ROB1";
        ch_A042_Channels.Ch_1.Ch_Nr:=1;
        !
        ! Channel 2
        ch_A042_Channels.Ch_2.T_Name:="";
        ch_A042_Channels.Ch_2.Ch_Nr:=2;
        !
        ! Channel 3
        ch_A042_Channels.Ch_3.T_Name:="";
        ch_A042_Channels.Ch_3.Ch_Nr:=3;
        !
        ! Channel 4
        ch_A042_Channels.Ch_4.T_Name:="";
        ch_A042_Channels.Ch_4.Ch_Nr:=4;
        !
        ! Master
        b_A042_AutoIPAddress:=TRUE;
        st_A042_IP_AddressMan:="192.168.125.1";
        st_A042_SerialNr:=GetSysInfo(\SerialNo);
        !
        ! Ports 
        b_A042_VirtualCustomPorts:=FALSE;
        n_A042_ViCustomSocketPortRec:=[31101,31102,31103,31104];
        n_A042_ViCustomSocketPortSen:=[31201,31202,31203,31204];
        !
        ! Roboter 1
        b_A042_Com{n_A042_R1_ChaNr}:=TRUE;
        b_A042_SIDCheck{n_A042_R1_ChaNr}:=TRUE;
        b_A042_SIDErrorStop{n_A042_R1_ChaNr}:=FALSE;
        b_A042_LogPro{n_A042_R1_ChaNr}:=FALSE;
        !
        ! Roboter 2
        b_A042_Com{n_A042_R2_ChaNr}:=FALSE;
        b_A042_SIDCheck{n_A042_R2_ChaNr}:=TRUE;
        b_A042_SIDErrorStop{n_A042_R2_ChaNr}:=FALSE;
        b_A042_LogPro{n_A042_R2_ChaNr}:=FALSE;
        !
        ! Roboter 3
        b_A042_Com{n_A042_R3_ChaNr}:=FALSE;
        b_A042_SIDCheck{n_A042_R3_ChaNr}:=FALSE;
        b_A042_SIDErrorStop{n_A042_R3_ChaNr}:=FALSE;
        b_A042_LogPro{n_A042_R3_ChaNr}:=TRUE;
        !
        ! Roboter 4
        b_A042_Com{n_A042_R4_ChaNr}:=FALSE;
        b_A042_SIDCheck{n_A042_R4_ChaNr}:=FALSE;
        b_A042_SIDErrorStop{n_A042_R4_ChaNr}:=FALSE;
        b_A042_LogPro{n_A042_R4_ChaNr}:=TRUE;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE