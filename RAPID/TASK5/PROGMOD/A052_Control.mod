MODULE A052_Control
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A052 Robot Beef
    !
    ! FUNCTION    :  First functions for developing  
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
    ! Function    :     Main for Project A052
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_Main()
        !
        ! Initialize cell
        r_A052_InitCell;
        !
        ! Production loop
        WHILE 1=1 DO
            !
            ! Placeholder for your code..
            WaitTime 1.0;
        ENDWHILE
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Inititialize cell 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_InitCell()
        !
        ! Clean teach pendat window
        TPErase;
        !
        ! Initialize signals
        r_A052_InitSig;
        !
        ! Initialize variables
        r_A052_InitVar;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Inititialize signals 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_InitSig()
        !
        ! Reset Signals

        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Inititialize variables 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_InitVar()
        !
        ! Reset variables
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE