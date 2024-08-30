@echo off
setlocal EnableDelayedExpansion

:: ��६���� ��� ������
set successCount=0
set failureCount=0

:: ��⠭���� ���䨪�⮢
call :InstallCertificate "%~dp0guc.crl" "root"
call :InstallCertificate "%~dp0guc_gost12.crl" "root"
call :InstallCertificate "%~dp0guc2021.crl" "root"
call :InstallCertificate "%~dp0guc2022.crl" "root"
call :InstallCertificate "%~dp0ucfk.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2020.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2021.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2021.crt" "ca"
call :InstallCertificate "%~dp0ucfk_2022.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2022.crt" "ca"
call :InstallCertificate "%~dp0ucfk_2022_1.1.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2022_1.1.crt" "ca"
call :InstallCertificate "%~dp0ucfk_2023.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2023.crt" "ca"
call :InstallCertificate "%~dp0ucfk_2024.crl" "ca"
call :InstallCertificate "%~dp0ucfk_2024.crt" "ca"
call :InstallCertificate "%~dp0ucfk_gost12.crl" "ca"
call :InstallCertificate "%~dp0Kornevoj_sertifikat_GUTs.crt" "root"
call :InstallCertificate "%~dp0Kornevoj_sertifikat_GUTs_2021.cer" "root"
call :InstallCertificate "%~dp0Kornevoj_sertifikat_GUTs_2022.cer" "root"
call :InstallCertificate "%~dp0Kornevoj_sertifikat_GUTs_GOST_2012.crt" "root"
call :InstallCertificate "%~dp0Podchinennyj_sertifikat_UTs_FK_GOST_2012.crt" "ca"
call :InstallCertificate "%~dp0Podchinennyj_sertifikat_UTs_FK_ot_04.07.2017.crt" "ca"
call :InstallCertificate "%~dp0Podchinennyj_sertifikat_UTs_FK_ot_05.02.2020.crt" "ca"

:: ���� � १�����
echo ==================================
echo ��⠭���� ���䨪�⮢ �����襭�.
echo �ᯥ��� ��⠭����: %successCount%
echo ��㤠��� ��⠭����: %failureCount%

pause
exit /b

:InstallCertificate
    set "certPath=%~1"
    set "certStore=%~2"

    :: �஢�ઠ �� ����� ��㬥���
    if "%certPath%"=="" (
        echo �訡��: ���� � ���䨪��� �� �����.
        set /a failureCount+=1
        exit /b
    )
    
    if "%certStore%"=="" (
        echo �訡��: �࠭���� ���䨪�� �� ������.
        set /a failureCount+=1
        exit /b
    )

    echo ��⠭���� ���䨪��: %certPath% � �࠭����: %certStore%

    certutil.exe -addstore -enterprise %certStore% "%certPath%" 2>&1
    
    if errorlevel 0 (
        echo ��⠭���� ���䨪�� ��諠 �ᯥ譮: %certPath%
        set /a successCount+=1
    ) else (
        echo �訡�� ��⠭���� ���䨪��: %certPath%
        set /a failureCount+=1
    )
exit /b
