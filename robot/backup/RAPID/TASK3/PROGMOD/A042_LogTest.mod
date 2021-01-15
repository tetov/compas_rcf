MODULE A042_LogTest

    !************************************************
    ! Declaration :     dir
    !************************************************
    !
    VAR dir dir_A042_DevExUSB;

    !************************************************
    ! Declaration :     iodev
    !************************************************
    !
    VAR iodev iodev_A042_LogFileExUSB;

    !************************************************
    ! Declaration :     string
    !************************************************
    !
    CONST string st_A042_LogDirPathExUSB:="RemovableDisk1:A042_Log/";
    ! C21_R21_R22_05-101052 on '192.168.0.21'/bd2:0
    ! C21_R21_R22_05-101052 on '192.168.0.21'/hd0a/C21_R21_R22_05-101052/HOME

    !************************************************
    ! Function    :     Test external USB Stick 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.04.25
    !***************** ETH Zürich *******************
    !
    PROC r_A042_TestExUSB_Stick()
        !
        ! Opent directory 
        OpenDir dir_A042_DevExUSB,st_A042_LogDirPathExUSB;
        !
        ! Check for log file 
        IF IsFile(st_A042_LogDirPathExUSB+st_A042_LogFileName+st_A042_LogFileFormat) THEN
            !
            ! Remove the old log file 
            RemoveFile st_A042_LogDirPathExUSB+st_A042_LogFileName+st_A042_LogFileFormat;
        ENDIF
        !
        ! Create and open a new log file 
        Open st_A042_LogDirPathExUSB+st_A042_LogFileName+st_A042_LogFileFormat,iodev_A042_LogFileExUSB\Write;
        !
        ! Write column title for 
        Write iodev_A042_LogFileExUSB,"L-Nr;LogTime;LogFormat;"\NoNewLine;
        !
        ! Close channel
        Close iodev_A042_LogFileExUSB;
        !
        ! Wait for closing channel complete
        WaitTime 5.0;
        !
        ! Log message 
        r_A042_EvLogMsg st_A042_LogFileName,"Log inititalizaion externel USB, done";
        !
        ! Temp end
        Stop;
        RETURN ;
    ERROR
        !
        ! Handle error open directory 
        IF ERRNO=ERR_FILEACC THEN
            !
            ! Create the log folder
            MakeDir st_A042_LogDirPathExUSB;
            !
            ! Log message 
            r_A042_EvLogMsg st_A042_LogFileName,"Log Directory externe USB created";
            !
            ! Retyry to open directory 
            RETRY;
        ENDIF
        Stop;
        Stop;
    ENDPROC


ENDMODULE