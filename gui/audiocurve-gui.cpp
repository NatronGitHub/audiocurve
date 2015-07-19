#include <QApplication>
#include "audiocurve-ui.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QCoreApplication::setApplicationName("AudioCurve");
    QCoreApplication::setOrganizationName("AudioCurve");
    QCoreApplication::setApplicationVersion(AUDIOCURVE_VERSION);
    a2a w;
    w.show();

    return a.exec();
}
