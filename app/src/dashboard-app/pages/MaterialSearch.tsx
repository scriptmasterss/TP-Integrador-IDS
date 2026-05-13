import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Search, ArrowLeft, Laptop, Book, Projector, Cable } from "lucide-react";

const mockInventory = [
  { id: 1, name: "Computadora Portátil Dell Latitude 5420", category: "Computadoras", available: 8, total: 15, icon: Laptop },
  { id: 2, name: "Computadora Portátil HP EliteBook 840", category: "Computadoras", available: 5, total: 10, icon: Laptop },
  { id: 3, name: "Análisis Matemático I - Protter & Morrey", category: "Libros", available: 12, total: 20, icon: Book },
  { id: 4, name: "Física I - Tipler & Mosca", category: "Libros", available: 7, total: 15, icon: Book },
  { id: 5, name: "Arduino UNO R3", category: "Placas", available: 15, total: 25, icon: Cable },
  { id: 6, name: "Raspberry Pi 4 Model B (4GB)", category: "Placas", available: 8, total: 12, icon: Cable },
  { id: 7, name: "Proyector Epson EB-X41", category: "Proyectores", available: 3, total: 5, icon: Projector },
  { id: 8, name: "Pantalla de Proyección Portátil 100\"", category: "Proyectores", available: 4, total: 6, icon: Projector },
  { id: 9, name: "Cable HDMI 2.0 (3m)", category: "Cables", available: 24, total: 30, icon: Cable },
  { id: 10, name: "Cable USB-C a USB-A (2m)", category: "Cables", available: 18, total: 25, icon: Cable },
  { id: 11, name: "Apuntes de Algoritmos y Programación II", category: "Apuntes", available: 30, total: 50, icon: Book },
  { id: 12, name: "Multímetro Digital Fluke 115", category: "Herramientas", available: 6, total: 8, icon: Cable },
];

export function MaterialSearch() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");

  const filteredItems = mockInventory.filter((item) => {
    const matchesSearch = item.name.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === "all" || item.category === category;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate("/alumno")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="font-semibold text-lg">Buscar Material</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Buscar en el Inventario</CardTitle>
            <CardDescription>Encuentra libros, computadoras, proyectores y más</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Input
                  placeholder="Buscar por nombre..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={category} onValueChange={setCategory}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Categoría" />
                </SelectTrigger>
                <SelectContent className="bg-white shadow-lg border">
                  <SelectItem value="all">Todas</SelectItem>
                  <SelectItem value="Computadoras">Computadoras</SelectItem>
                  <SelectItem value="Libros">Libros</SelectItem>
                  <SelectItem value="Apuntes">Apuntes</SelectItem>
                  <SelectItem value="Placas">Placas</SelectItem>
                  <SelectItem value="Proyectores">Proyectores</SelectItem>
                  <SelectItem value="Cables">Cables</SelectItem>
                  <SelectItem value="Herramientas">Herramientas</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredItems.map((item) => {
            const Icon = item.icon;
            const availabilityPercent = (item.available / item.total) * 100;
            return (
              <Card key={item.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <Icon className="w-6 h-6 text-blue-600" />
                    </div>
                    <Badge variant={item.available > 0 ? "default" : "destructive"}>
                      {item.available} / {item.total}
                    </Badge>
                  </div>
                  <CardTitle className="text-base mt-3">{item.name}</CardTitle>
                  <CardDescription>{item.category}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Disponibilidad</span>
                        <span className="font-medium">{availabilityPercent.toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            availabilityPercent > 50 ? "bg-green-500" : availabilityPercent > 20 ? "bg-yellow-500" : "bg-red-500"
                          }`}
                          style={{ width: `${availabilityPercent}%` }}
                        />
                      </div>
                    </div>
                    <Button
                      className="w-full bg-slate-900/10 backdrop-blur-md border border-slate-200 text-slate-900 font-bold hover:bg-slate-900 hover:text-white transition-all duration-300"
                      disabled={item.available === 0}
                      onClick={() => navigate(`/prestamo/new-${item.id}`)}
                    >
                      {item.available > 0 ? "Solicitar Préstamo" : "No Disponible"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {filteredItems.length === 0 && (
          <Card className="p-12 text-center">
            <p className="text-gray-500">No se encontraron resultados para tu búsqueda</p>
          </Card>
        )}
      </main>
    </div>
  );
}
