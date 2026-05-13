import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import {
  BookOpen,
  TrendingUp,
  AlertCircle,
  Users,
  Package,
  BarChart3,
  Download,
  CheckCircle,
  XCircle,
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

const demandByCareer = [
  { career: "Informática", loans: 145 },
  { career: "Civil", loans: 89 },
  { career: "Electrónica", loans: 112 },
  { career: "Mecánica", loans: 67 },
  { career: "Industrial", loans: 78 },
];

const topItems = [
  { name: "Arduino UNO", count: 45, category: "Placas" },
  { name: "Laptop Dell", count: 38, category: "Computadoras" },
  { name: "Análisis Matemático I", count: 32, category: "Libros" },
  { name: "Proyector Epson", count: 28, category: "Proyectores" },
  { name: "Cable HDMI", count: 24, category: "Cables" },
];

const inventoryStatus = [
  { name: "Disponible", value: 342, color: "#10b981" },
  { name: "Prestado", value: 128, color: "#3b82f6" },
  { name: "Mantenimiento", value: 15, color: "#f59e0b" },
  { name: "Perdido/Dañado", value: 8, color: "#ef4444" },
];

const lateLoan = [
  {
    id: "PR-2024-032",
    student: "María González",
    studentId: "104521",
    item: "Raspberry Pi 4",
    dueDate: "2026-05-05",
    daysLate: 7,
  },
  {
    id: "PR-2024-018",
    student: "Carlos Rodríguez",
    studentId: "102874",
    item: "Análisis Matemático II",
    dueDate: "2026-05-08",
    daysLate: 4,
  },
  {
    id: "PR-2024-045",
    student: "Ana Martínez",
    studentId: "105692",
    item: "Multímetro Fluke",
    dueDate: "2026-05-09",
    daysLate: 3,
  },
];

const pendingRequests = [
  {
    id: "PR-2024-089",
    student: "Pedro López",
    studentId: "103456",
    item: "Computadora HP EliteBook",
    requestDate: "2026-05-12 09:30",
  },
  {
    id: "PR-2024-090",
    student: "Laura Fernández",
    studentId: "104987",
    item: "Proyector Epson EB-X41",
    requestDate: "2026-05-12 10:15",
  },
];

export function AdminDashboard() {
  const navigate = useNavigate();
  const [selectedCareer, setSelectedCareer] = useState("all");

  const handleGenerateReport = () => {
    alert("En un sistema real, esto generaría un PDF con el reporte de morosidad");
  };

  const handleApprove = (id: string) => {
    alert(`Préstamo ${id} aprobado`);
  };

  const handleReject = (id: string) => {
    alert(`Préstamo ${id} rechazado`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-semibold text-lg">Panel de Administración</h1>
              <p className="text-sm text-gray-600">Biblioteca FIUBA</p>
            </div>
          </div>
          <Button variant="outline" onClick={() => navigate("/")}>
            Cerrar Sesión
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Préstamos Activos</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <p className="text-3xl font-bold">128</p>
                <Package className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Usuarios Activos</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <p className="text-3xl font-bold">342</p>
                <Users className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Préstamos Pendientes</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <p className="text-3xl font-bold">{pendingRequests.length}</p>
                <AlertCircle className="w-8 h-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Devoluciones Atrasadas</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <p className="text-3xl font-bold">{lateLoan.length}</p>
                <AlertCircle className="w-8 h-8 text-red-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="analytics" className="space-y-6">
          <TabsList>
            <TabsTrigger value="analytics">
              <BarChart3 className="w-4 h-4 mr-2" />
              Análisis
            </TabsTrigger>
            <TabsTrigger value="pending">
              <AlertCircle className="w-4 h-4 mr-2" />
              Solicitudes Pendientes
            </TabsTrigger>
            <TabsTrigger value="late">
              <AlertCircle className="w-4 h-4 mr-2" />
              Morosidad
            </TabsTrigger>
          </TabsList>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Demanda por Carrera</CardTitle>
                      <CardDescription>Préstamos totales por carrera</CardDescription>
                    </div>
                    <Select value={selectedCareer} onValueChange={setSelectedCareer}>
                      <SelectTrigger className="w-32">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-white shadow-lg border">
                        <SelectItem value="all">Todas</SelectItem>
                        <SelectItem value="informatica">Informática</SelectItem>
                        <SelectItem value="civil">Civil</SelectItem>
                        <SelectItem value="electronica">Electrónica</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={demandByCareer}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="career" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="loans" fill="#3b82f6" name="Préstamos" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Estado del Inventario</CardTitle>
                  <CardDescription>Distribución actual de materiales</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={inventoryStatus}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value }) => `${name}: ${value}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {inventoryStatus.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                  <CardTitle>Material Más Solicitado</CardTitle>
                </div>
                <CardDescription>Top 5 items más prestados del mes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {topItems.map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-white border border-blue-100 rounded-lg shadow-sm hover:border-blue-400 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="bg-blue-100 text-blue-600 rounded-full w-8 h-8 flex items-center justify-center font-bold">
                          {index + 1}
                        </div>
                        <div>
                          <p className="font-medium">{item.name}</p>
                          <p className="text-sm text-gray-600">{item.category}</p>
                        </div>
                      </div>
                      <Badge>{item.count} préstamos</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="pending">
            <Card>
              <CardHeader>
                <CardTitle>Solicitudes Pendientes de Aprobación</CardTitle>
                <CardDescription>Revisa y aprueba las solicitudes de préstamo</CardDescription>
              </CardHeader>
              <CardContent>
                {pendingRequests.length > 0 ? (
                  <div className="space-y-4">
                    {pendingRequests.map((request) => (
                      <Card key={request.id} className="border-orange-200 bg-orange-50">
                        <CardContent className="pt-6">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <p className="font-semibold">{request.item}</p>
                              <p className="text-sm text-gray-600 mt-1">ID: {request.id}</p>
                              <div className="mt-2 space-y-1">
                                <p className="text-sm">
                                  <strong>Alumno:</strong> {request.student}
                                </p>
                                <p className="text-sm">
                                  <strong>Padrón:</strong> {request.studentId}
                                </p>
                                <p className="text-sm">
                                  <strong>Solicitado:</strong> {request.requestDate}
                                </p>
                              </div>
                            </div>
                            <div className="flex gap-2">
                              <Button
                                size="sm"
                                className="bg-green-600 hover:bg-green-700"
                                onClick={() => handleApprove(request.id)}
                              >
                                <CheckCircle className="w-4 h-4 mr-1" />
                                Aprobar
                              </Button>
                              <Button
                                size="sm"
                                variant="destructive"
                                className="bg-red-600 hover:bg-red-700 text-white"
                                onClick={() => handleReject(request.id)}
                              >
                                <XCircle className="w-4 h-4 mr-1" />
                                Rechazar
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    No hay solicitudes pendientes
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="late">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Reporte de Morosidad</CardTitle>
                    <CardDescription>
                      Alumnos con devoluciones pendientes fuera de plazo
                    </CardDescription>
                  </div>
                  <Button onClick={handleGenerateReport}>
                    <Download className="w-4 h-4 mr-2" />
                    Generar PDF
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {lateLoan.map((loan) => (
                    <Card key={loan.id} className="border-red-200 bg-red-50">
                      <CardContent className="pt-6">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className="font-semibold">{loan.item}</p>
                            <p className="text-sm text-gray-600 mt-1">ID: {loan.id}</p>
                            <div className="mt-2 space-y-1">
                              <p className="text-sm">
                                <strong>Alumno:</strong> {loan.student}
                              </p>
                              <p className="text-sm">
                                <strong>Padrón:</strong> {loan.studentId}
                              </p>
                              <p className="text-sm">
                                <strong>Vencimiento:</strong>{" "}
                                {new Date(loan.dueDate).toLocaleDateString('es-AR')}
                              </p>
                            </div>
                          </div>
                          <Badge variant="destructive" className="text-lg text-red-600 font-bold bg-white border-red-600">
                            {loan.daysLate} días de retraso
                          </Badge>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
