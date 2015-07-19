#include "audiocurve-ui.h"
#include "ui_audiocurve-gui.h"
#include <QMessageBox>
#include <QFileDialog>
#include <QDir>
#include <QFile>
#include <QFileDialog>
#include <QTextStream>
#include <QSettings>
#include <QTimer>

a2a::a2a(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::a2a)
{
    ui->setupUi(this);
    resetParams();
    connect(&audio,SIGNAL(error(QString)),this,SLOT(errorHandler(QString)));
    connect(&audio,SIGNAL(status(QString)),this,SLOT(statusHandler(QString)));
    QTimer::singleShot(0,this,SLOT(loadConf()));
}

a2a::~a2a()
{
    saveConf();
    delete ui;
}

void a2a::loadConf()
{
    QSettings settings;
    settings.beginGroup("ui");
    if (settings.value("state").isValid())
        this->restoreState(settings.value("state").toByteArray());
    if (settings.value("size").isValid())
        this->resize(settings.value("size",QSize(320,256)).toSize());
    if (settings.value("pos").isValid())
        this->move(settings.value("pos",QPoint(0,0)).toPoint());
    if (settings.value("max").toBool() == true)
        this->showMaximized();
    settings.endGroup();
    settings.beginGroup("file");
    if (!settings.value("lastDir").isNull())
        lastDir = settings.value("lastDir").toString();
    settings.endGroup();

    if (audio.bin().isEmpty()) {
        QMessageBox::warning(this,tr("SoX is missing"),tr("SoX is missing, please install Sox and restart program"));
        QTimer::singleShot(0,qApp,SLOT(quit()));
    }
}

void a2a::saveConf()
{
    QSettings settings;
    settings.beginGroup("ui");
    settings.setValue( "state",this->saveState());
    settings.setValue("size",this->size());
    settings.setValue("pos",this->pos());
    if (this->isMaximized())
        settings.setValue("max","true");
    else
        settings.setValue("max","false");
    settings.endGroup();
    settings.beginGroup("file");
    if (!lastDir.isEmpty())
        settings.setValue("lastDir",lastDir);
    settings.endGroup();
}

void a2a::on_actionAboutApp_triggered()
{
    QMessageBox::about(this,"About "+qApp->applicationName(),"<h3>"+qApp->applicationName()+" "+qApp->applicationVersion()+"</h3><p>Audio curve generator for Natron.</p><p>Made by <a href=\"https://github.com/olear\">olear</a> and <a href=\"https://github.com/rcspam\">rcspam</a>.</p>"+audio.about());
}

void a2a::on_actionAboutQt_triggered()
{
    QMessageBox::aboutQt(this);
}

void a2a::on_actionOpen_triggered()
{
    if (!ui->reload->isHidden())
        ui->reload->hide();
    QString openDir;
    if (!lastDir.isEmpty())
        openDir = lastDir;
    else
        openDir = QDir::homePath();
    QString audioFormats;
    audioFormats = audio.formats();
    if (audioFormats.isEmpty())
        audioFormats.append("*.wav");
    QString fileName = QFileDialog::getOpenFileName(this,tr("Open audio file"), openDir, tr("Audio Files")+" ("+audioFormats+")");
    if (!fileName.isEmpty()) {
        active = fileName;
        QFileInfo file(fileName);
        lastDir = file.absolutePath();
        int length = audio.duration(active,0);
        if (length>0) {
            ui->spinBox_duration->setMinimum(0);
            ui->spinBox_duration->setMaximum(length);
            ui->spinBox_duration->setValue(length);
            ui->sliderDuration->setMinimum(0);
            ui->sliderDuration->setMaximum(length);
            ui->sliderDuration->setValue(length);
        }
        else {
            ui->spinBox_duration->setMinimum(0);
            ui->spinBox_duration->setMaximum(1000);
            ui->spinBox_duration->setValue(10);
            ui->sliderDuration->setMinimum(0);
            ui->sliderDuration->setMaximum(1000);
            ui->sliderDuration->setValue(10);
        }
        getData();
    }
}

void a2a::on_actionSave_triggered()
{
    if (!ui->reload->isHidden())
        ui->reload->hide();
    if (!ui->output->toPlainText().isEmpty()) {
        QString fileName = QFileDialog::getSaveFileName(this,tr("Save text file"), lastDir, tr("Text File (*.txt)"));
        if (!fileName.isEmpty()) {
            QFile output(fileName);
            if (output.open(QIODevice::WriteOnly|QIODevice::Text)) {
                QTextStream stream(&output);
                stream << ui->output->toPlainText();
                output.close();
            }
            if (output.exists()) {
                ui->statusBar->showMessage(tr("Text file saved"),5000);
                ui->actionSave->setEnabled(false);
            }
            else
                ui->statusBar->showMessage(tr("Failed to save text file"),5000);
        }
    }
    else
        ui->statusBar->showMessage(tr("Nothing to save"),5000);
}

void a2a::on_actionQuit_triggered()
{
    qApp->quit();
}

void a2a::resetParams()
{
    ui->spinBox_duration->clear();
    ui->spinBox_fps->clear();
    ui->output->clear();
    ui->curveX->setChecked(true);
    ui->curveY->setChecked(false);
    this->setWindowTitle(qApp->applicationName());
    ui->spinBox_fps->setValue(24);
    ui->spinBox_duration->setMaximum(0);
    ui->spinBox_duration->setMinimum(0);
    ui->spinBox_duration->setValue(0);
    ui->sliderDuration->setMaximum(0);
    ui->sliderDuration->setMinimum(0);
    ui->sliderDuration->setValue(0);
    ui->curveXFactor->setValue(100);
    ui->curveYFactor->setValue(100);
    ui->actionOpen->setEnabled(true);
    ui->actionSave->setEnabled(false);
    active.clear();
    ui->output->setFocus();
    ui->reload->hide();
    ui->labelDuration->setText("(0 frames)");
}

void a2a::getData()
{
    if (!ui->reload->isHidden())
        ui->reload->hide();
    ui->actionSave->setDisabled(true);
    ui->actionOpen->setDisabled(true);
    if (!active.isEmpty()) {
        qApp->processEvents();
        QString result = audio.dat(active,ui->spinBox_fps->value(),ui->spinBox_duration->value()*ui->spinBox_fps->value(),ui->curveX->isChecked(),ui->curveY->isChecked(),ui->curveXFactor->value(),ui->curveYFactor->value(),false);
        if (!result.isEmpty()) {
            ui->output->setPlainText(result);
            ui->actionSave->setEnabled(true);
            ui->actionOpen->setEnabled(true);
            ui->output->setEnabled(true);
            this->setWindowTitle(qApp->applicationName()+" "+active);
        }
    }
    else {
        ui->statusBar->showMessage(tr("No result"),5000);
        active.clear();
        ui->output->clear();
        ui->output->setEnabled(false);
        ui->actionSave->setEnabled(false);
        ui->actionSave->setEnabled(true);
    }
}

void a2a::errorHandler(QString error)
{
    if (!error.isEmpty()) {
        QMessageBox::warning(this,tr("Warning"),error);
        resetParams();
    }
}

void a2a::statusHandler(QString status)
{
    if (!status.isEmpty())
        ui->statusBar->showMessage(status,5000);
}

void a2a::on_reload_clicked()
{
    if (!ui->reload->isHidden() && !active.isEmpty()) {
        ui->reload->hide();
        getData();
    }
}

void a2a::on_spinBox_duration_valueChanged(int arg1)
{
    if (ui->reload->isHidden() && !active.isEmpty())
        ui->reload->show();
    ui->sliderDuration->setValue(arg1);
    ui->labelDuration->setText("("+QString::number(ui->spinBox_duration->value()*ui->spinBox_fps->value())+" frames)");
}

void a2a::on_sliderDuration_valueChanged(int value)
{
    ui->spinBox_duration->setValue(value);
}

void a2a::on_curveX_stateChanged(int arg1)
{
    Q_UNUSED(arg1)
    if (ui->reload->isHidden() && !active.isEmpty())
        ui->reload->show();
}

void a2a::on_curveY_stateChanged(int arg1)
{
    Q_UNUSED(arg1)
    if (ui->reload->isHidden() && !active.isEmpty())
        ui->reload->show();
}

void a2a::on_curveXFactor_valueChanged(int arg1)
{
    Q_UNUSED(arg1)
    if (ui->reload->isHidden() && !active.isEmpty())
        ui->reload->show();
}

void a2a::on_curveYFactor_valueChanged(int arg1)
{
    Q_UNUSED(arg1)
    if (ui->reload->isHidden() && !active.isEmpty())
        ui->reload->show();
}

void a2a::on_actionClear_triggered()
{
    resetParams();
}

void a2a::on_spinBox_fps_valueChanged(double arg1)
{
    if (ui->reload->isHidden() && !active.isEmpty())
        ui->reload->show();
    ui->sliderFPS->setValue(arg1);
    ui->labelDuration->setText("("+QString::number(ui->spinBox_duration->value()*ui->spinBox_fps->value())+" frames)");
}

void a2a::on_sliderFPS_sliderMoved(int position)
{
    ui->spinBox_fps->setValue(position);
}
