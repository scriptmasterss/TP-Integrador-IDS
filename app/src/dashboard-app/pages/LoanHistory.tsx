import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { ArrowLeft, Calendar, Package } from "lucide-react";

const mockHistory = [
  {
    id: "PR-2024-001",
    item: "Computadora Portátil Dell",
    requestDate: "2026-05-10",
    dueDate: "2026-05-15",
    returnDate: null,
    status: "active",
  },
  {
    id: "PR-2024-045",
    item: "Arduino UNO R3",
    requestDate: "2026-04-20",
    dueDate: "2026-04-27",
    returnDate: "2026-04-26",
    status: "returned",
  },
  {
    id: "PR-2024-032",
    item: "Análisis Matemático I - Protter",
    requestDate: "2026-03-15",
    dueDate: "2026-04-15",
    returnDate: "2026-04-18",
    status: "late",
  },
  {
    id: "PR-2024-018",
    item: "Proyector Epson EB-X41",
    requestDate: "2026-03-05",
    dueDate: "2026-03-06",
    returnDate: "2026-03-06",
    status: "returned",
  },
  {
    id: "PR-2024-007",
    item: "Cable HDMI 2.0 (3m)",
    requestDate: "2026-02-12",
    dueDate: "2026-02-19",
    returnDate: "2026-02-19",
    status: "returned",
  },
];

export function LoanHistory() {
  const navigate = useNavigate();

  const activeLoan = mockHistory.filter((loan) => loan.status === "active");
  const completedLoans = mockHistory.filter((loan) => loan.status !== "active");

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-blue-500">Activo</Badge>;
      case "returned":
        return <Badge className="bg-green-500">Devuelto</Badge>;
      case "late":
        return <Badge variant="destructive">Devuelto con Retraso</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const LoanCard = ({ loan }: { loan: typeof mockHistory[0] }) => (
    <Card className="mb-4">
      <CardContent className="pt-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Package className="w-4 h-4 text-gray-600" />
              <p className="font-semibold">{loan.item}</p>
            </div>
            <p className="text-sm text-gray-600 mb-1">ID: {loan.id}</p>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                <span>Solicitado: {new Date(loan.requestDate).toLocaleDateString('es-AR')}</span>
              </div>
              <div>
                Vencimiento: {new Date(loan.dueDate).toLocaleDateString('es-AR')}
              </div>
            </div>
            {loan.returnDate && (
              <p className="text-sm text-gray-600 mt-1">
                Devuelto: {new Date(loan.returnDate).toLocaleDateString('es-AR')}
              </p>
            )}
          </div>
          <div className="flex flex-col items-end gap-2">
            {getStatusBadge(loan.status)}
            {loan.status === "active" && (
              <Button size="sm" onClick={() => navigate(`/prestamo/${loan.id}`)}>
                Ver Detalles
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate("/alumno")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="font-semibold text-lg">Mi Historial de Préstamos</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <Tabs defaultValue="active" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="active">
              Activos ({activeLoan.length})
            </TabsTrigger>
            <TabsTrigger value="completed">
              Histórico ({completedLoans.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="active">
            <Card>
              <CardHeader>
                <CardTitle>Préstamos Activos</CardTitle>
              </CardHeader>
              <CardContent>
                {activeLoan.length > 0 ? (
                  activeLoan.map((loan) => <LoanCard key={loan.id} loan={loan} />)
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    No tienes préstamos activos
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="completed">
            <Card>
              <CardHeader>
                <CardTitle>Historial Completo</CardTitle>
              </CardHeader>
              <CardContent>
                {completedLoans.map((loan) => (
                  <LoanCard key={loan.id} loan={loan} />
                ))}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
