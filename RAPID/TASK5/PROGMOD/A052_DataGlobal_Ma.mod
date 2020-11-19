MODULE A052_DataGlobal_Ma
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A052 Robot Beefer
    !
    ! FUNCTION    :  Modul includs all global data  
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.03.28 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2018
    !                - Philippe Fleischmann
    !                - Michael Lyrenmann
    !                - Matthias Kohler 
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
    PERS bool b_A052_StartGrill:=FALSE;
    PERS bool b_A052_GrillSide1:=TRUE;
    PERS bool b_A052_GrillSide2:=FALSE;

    !************************************************
    ! Declaration :     num
    !************************************************
    !
    PERS num n_A052_GrillTimeSide1:=33;
    PERS num n_A052_GrillTimeSide2:=33;
    PERS num n_A052_CurrentBeefTime:=0;
    PERS num n_A052_MaxBeefTime:=26;
    
    !************************************************
    ! Declaration :     string
    !************************************************
    !

ENDMODULE