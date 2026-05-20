import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Upload } from "lucide-react";

export function PersonalDataPage() {
  const navigate = useNavigate();
  const studentType = localStorage.getItem("studentType") || "general";
  const [formData, setFormData] = useState({
    nombre: "",
    apellidoPaterno: "",
    apellidoMaterno: "",
    fechaNacimiento: "",
    curp: "",
    genero: "",
    numeroCuenta: "",
    facultad: "",
    licenciatura: "",
    generacion: "",
    semestre: "",
  });
  const [documento, setDocumento] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem("personalData", JSON.stringify(formData));
    navigate("/tipo-tramite");
  };

  const getDocumentLabel = () => {
    switch (studentType) {
      case "fca":
        return "Credencial FCA";
      case "unam":
        return "Credencial UNAM";
      case "general":
        return "Identificación Oficial";
      default:
        return "Documento";
    }
  };

  const showUNAMFields = studentType === "fca" || studentType === "unam";

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Datos Personales
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="nombre">Nombre(s)</Label>
              <Input
                id="nombre"
                value={formData.nombre}
                onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                required
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="apellidoPaterno">Apellido Paterno</Label>
              <Input
                id="apellidoPaterno"
                value={formData.apellidoPaterno}
                onChange={(e) => setFormData({ ...formData, apellidoPaterno: e.target.value })}
                required
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="apellidoMaterno">Apellido Materno</Label>
              <Input
                id="apellidoMaterno"
                value={formData.apellidoMaterno}
                onChange={(e) => setFormData({ ...formData, apellidoMaterno: e.target.value })}
                required
                className="mt-1"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="fechaNacimiento">Fecha de Nacimiento</Label>
              <Input
                id="fechaNacimiento"
                type="date"
                value={formData.fechaNacimiento}
                onChange={(e) => setFormData({ ...formData, fechaNacimiento: e.target.value })}
                required
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="curp">CURP</Label>
              <Input
                id="curp"
                value={formData.curp}
                onChange={(e) => setFormData({ ...formData, curp: e.target.value.toUpperCase() })}
                required
                className="mt-1"
                maxLength={18}
              />
            </div>
          </div>

          <div>
            <Label htmlFor="genero">Género</Label>
            <Select
              value={formData.genero}
              onValueChange={(value) => setFormData({ ...formData, genero: value })}
            >
              <SelectTrigger className="mt-1">
                <SelectValue placeholder="Selecciona género" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="masculino">Masculino</SelectItem>
                <SelectItem value="femenino">Femenino</SelectItem>
                <SelectItem value="otro">Otro</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {showUNAMFields && (
            <>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="numeroCuenta">Número de Cuenta</Label>
                  <Input
                    id="numeroCuenta"
                    value={formData.numeroCuenta}
                    onChange={(e) => setFormData({ ...formData, numeroCuenta: e.target.value })}
                    required
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="facultad">Facultad</Label>
                  <Input
                    id="facultad"
                    value={formData.facultad}
                    onChange={(e) => setFormData({ ...formData, facultad: e.target.value })}
                    required
                    className="mt-1"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="licenciatura">Licenciatura</Label>
                  <Input
                    id="licenciatura"
                    value={formData.licenciatura}
                    onChange={(e) => setFormData({ ...formData, licenciatura: e.target.value })}
                    required
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="generacion">Generación</Label>
                  <Input
                    id="generacion"
                    value={formData.generacion}
                    onChange={(e) => setFormData({ ...formData, generacion: e.target.value })}
                    required
                    className="mt-1"
                    placeholder="2024"
                  />
                </div>
                <div>
                  <Label htmlFor="semestre">Semestre</Label>
                  <Select
                    value={formData.semestre}
                    onValueChange={(value) => setFormData({ ...formData, semestre: value })}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Semestre" />
                    </SelectTrigger>
                    <SelectContent>
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((sem) => (
                        <SelectItem key={sem} value={sem.toString()}>
                          {sem}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </>
          )}

          <div>
            <Label htmlFor="documento">{getDocumentLabel()}</Label>
            <div className="mt-1 flex items-center gap-4">
              <Input
                id="documento"
                type="file"
                onChange={(e) => setDocumento(e.target.files?.[0] || null)}
                required
                accept=".pdf,.jpg,.jpeg,.png"
                className="flex-1"
              />
              <Upload className="w-5 h-5 text-gray-400" />
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Formatos aceptados: PDF, JPG, PNG (máx. 5MB)
            </p>
          </div>

          <Button type="submit" className="w-full">
            Continuar
          </Button>
        </form>
      </div>
    </div>
  );
}
