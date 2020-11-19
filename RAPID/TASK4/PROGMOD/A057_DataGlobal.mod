MODULE A057_DataGlobal
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIB C51 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A057 MAS Rio
    !
    ! FUNCTION    :  Includ all Global Data's for Project
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2020.01.27
    !
    ! Copyright   :  ETH Zürich (CH) 2019
    !
    !***********************************************************************************

    !************************************************
    ! Declaration :     bool
    !************************************************
    !
    PERS bool b_A057_Run;
    PERS bool b_A057_MaWaitForJob;
    PERS bool b_A057_MaInUse;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    PERS num n_A057_AccRamp;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    PERS string st_A057_JobForMa:=" ";

    !************************************************
    ! Declaration :     speeddata
    !************************************************
    !
    PERS speeddata v_A057_Max;
    PERS speeddata v_A057_Med;
    PERS speeddata v_A057_Min;

    !************************************************
    ! Declaration :     speedlimdata
    !************************************************
    !
    PERS speedlimdata slim_A057_Master;

    !************************************************
    ! Declaration :     syncident
    !************************************************
    !
    !
    VAR syncident id_A057_MainSta;
    VAR syncident id_A057_MainEnd;
    !
    VAR syncident id_A057_InitTaskSta;
    VAR syncident id_A057_InitTaskEnd;
    !
    VAR syncident id_A057_InitVarSta;
    VAR syncident id_A057_InitVarEnd;
    !
    VAR syncident id_A057_InitSigSta;
    VAR syncident id_A057_InitSigEnd;
    !
    VAR syncident id_A057_InitSpeedSta;
    VAR syncident id_A057_InitSpeedSet;
    VAR syncident id_A057_InitSpeedEnd;

ENDMODULE