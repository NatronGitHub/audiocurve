QT       += core gui
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = AudioCurveGUI
VERSION = 1.0
TEMPLATE = app

SOURCES += audiocurve-gui.cpp audiocurve-ui.cpp ../sox.cpp
HEADERS  += audiocurve-ui.h ../sox.h
FORMS    += audiocurve-gui.ui
RESOURCES += audiocurve-gui.qrc

QMAKE_TARGET_DESCRIPTION="Audio Curve Generator"
QMAKE_TARGET_COPYRIGHT="Copyright 2015 @olear and @rcspam"
QMAKE_TARGET_PRODUCT="audiocurve"

QMAKE_CLEAN += Makefile target
DEFINES += AUDIOCURVE_VERSION=\"\\\"$${VERSION}\\\"\"

lessThan(QT_MAJOR_VERSION, 5): win32:RC_FILE += audiocurve-gui.rc
greaterThan(QT_MAJOR_VERSION, 4):win32:RC_ICONS += audiocurve.ico

DESTDIR = build
OBJECTS_DIR = $$DESTDIR/tmp
MOC_DIR = $$DESTDIR/tmp
RCC_DIR = $$DESTDIR/tmp
UI_DIR = $$DESTDIR/tmp

unix {
    isEmpty(PREFIX) {
        PREFIX = /usr/local
    }
    isEmpty(DOCDIR) {
        DOCDIR = $${PREFIX}/share/doc
    }
    target.path = $${PREFIX}/bin
    target_icon.path = $${PREFIX}/share/pixmaps
    target_icon.files = audiocurve.png
    target_desktop.path = $${PREFIX}/share/applications
    target_desktop.files = audiocurve.desktop
    target_docs.path = $${DOCDIR}/audiocurve-$${VERSION}
    target_docs.files = README.md LICENSE
    target_script.path = $${PREFIX}/bin
    INSTALLS += target target_icon target_desktop target_docs
}
