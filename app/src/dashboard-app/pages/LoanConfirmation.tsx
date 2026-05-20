import { useNavigate, useParams } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { ArrowLeft, Calendar, User, Package, QrCode, Download } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";

export function LoanConfirmation() {
  const navigate = useNavigate();
  const { id } = useParams();

  const loanData = {
    id: id || "PR-2024-001",
    item: "Computadora Portátil Dell Latitude 5420",
    category: "Computadoras",
    student: "Juan Pérez",
    studentId: "103456",
    career: "Ingeniería Informática",
    requestDate: "2026-05-10T10:30:00",
    approvedDate: "2026-05-10T11:15:00",
    pickupDate: "2026-05-10T14:00:00",
    dueDate: "2026-05-15T18:00:00",
    status: "active",
    qrCode: `LOAN-${id}-FIUBA-2026`,
  };

  const handleDownloadPDF = () => {
    alert("En un sistema real, esto generaría un PDF con los detalles del préstamo");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate("/alumno")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="font-semibold text-lg">Detalles del Préstamo</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="text-2xl">{loanData.item}</CardTitle>
                <CardDescription className="mt-2">
                  {loanData.category} • ID: {loanData.id}
                </CardDescription>
              </div>
              <Badge className="bg-blue-500">Activo</Badge>
            </div>
          </CardHeader>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <User className="w-5 h-5 text-blue-600" />
                <CardTitle>Información del Alumno</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-2">
              <div>
                <p className="text-sm text-gray-600">Nombre</p>
                <p className="font-medium">{loanData.student}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Padrón</p>
                <p className="font-medium">{loanData.studentId}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Carrera</p>
                <p className="font-medium">{loanData.career}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-blue-600" />
                <CardTitle>Fechas Importantes</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-2">
              <div>
                <p className="text-sm text-gray-600">Solicitado</p>
                <p className="font-medium">
                  {new Date(loanData.requestDate).toLocaleString('es-AR')}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Aprobado</p>
                <p className="font-medium">
                  {new Date(loanData.approvedDate).toLocaleString('es-AR')}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Fecha de Devolución</p>
                <p className="font-medium text-orange-600">
                  {new Date(loanData.dueDate).toLocaleString('es-AR')}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <QrCode className="w-5 h-5 text-blue-600" />
              <CardTitle>Código QR del Préstamo</CardTitle>
            </div>
            <CardDescription>
              Presenta este código para confirmar la entrega y devolución del material
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center gap-4">
              <div className="bg-white p-6 rounded-lg border-2 border-gray-200">
                <QRCodeSVG
                  value={loanData.qrCode}
                  size={200}
                  level="H"
                  includeMargin={true}
                />
              </div>
              <p className="text-sm text-gray-600 text-center">
                Código: {loanData.qrCode}
              </p>
              <div className="flex gap-3">
                <Button variant="outline" onClick={handleDownloadPDF}>
                  <Download className="w-4 h-4 mr-2" />
                  Descargar PDF
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-blue-50 border-blue-200">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Package className="w-5 h-5 text-blue-600" />
              <CardTitle>Instrucciones</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <p>
              <strong>Para retirar el material:</strong> Acércate a la biblioteca con tu
              documento y presenta este código QR al bibliotecario.
            </p>
            <p>
              <strong>Para devolver el material:</strong> Regresa a la biblioteca antes
              de la fecha de devolución y presenta nuevamente el código QR.
            </p>
            <p className="text-orange-600">
              <strong>Importante:</strong> Los retrasos en la devolución pueden resultar
              en sanciones y restricciones para futuros préstamos.
            </p>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
