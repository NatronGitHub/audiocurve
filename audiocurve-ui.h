#ifndef A2A_H
#define A2A_H

#include <QMainWindow>
#include "sox.h"

namespace Ui {
class a2a;
}

class a2a : public QMainWindow
{
    Q_OBJECT

public:
    explicit a2a(QWidget *parent = 0);
    ~a2a();

private slots:
    void on_actionAboutApp_triggered();
    void on_actionAboutQt_triggered();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();
    void on_actionQuit_triggered();
    void resetParams();
    void getData();
    void errorHandler(QString error);
    void statusHandler(QString status);
    void on_reload_clicked();
    void on_spinBox_duration_valueChanged(int arg1);
    void on_spinBox_fps_valueChanged(int arg1);
    void loadConf();
    void saveConf();
    void on_sliderFPS_valueChanged(int value);
    void on_sliderDuration_valueChanged(int value);
    void on_curveX_stateChanged(int arg1);
    void on_curveY_stateChanged(int arg1);
    void on_curveXFactor_valueChanged(int arg1);
    void on_curveYFactor_valueChanged(int arg1);
    void on_actionClear_triggered();

private:
    Ui::a2a *ui;
    Sox audio;
    QString active;
    QString lastDir;
};

#endif // A2A_H
