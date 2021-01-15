MODULE A057_DataGlobal_Ma
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
    !
    !************************************************
    ! Declaration :     bool
    !************************************************
    !
    PERS bool b_A057_Run:=TRUE;
    PERS bool b_A057_MaWaitForJob:=TRUE;
    PERS bool b_A057_MaInUse:=FALSE;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    PERS num n_A057_AccRamp:=33;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    PERS string st_A057_JobForMa:=" ";

    !************************************************
    ! Declaration :     speeddata
    !************************************************
    !
    PERS speeddata v_A057_Max:=[400,100,400,10];
    PERS speeddata v_A057_Med:=[250,50,250,10];
    PERS speeddata v_A057_Min:=[50,25,250,10];

    !************************************************
    ! Declaration :     speedlimdata
    !************************************************
    !
    PERS speedlimdata slim_A057_Master:=[600,28,14,19,19,31,29,0,0,0,0,0,0];

    !************************************************
    ! Declaration :     syncident
    !************************************************
    !
    !
    VAR syncident id_A057_MainSta;
    VAR syncident id_A057_MainEnd;

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