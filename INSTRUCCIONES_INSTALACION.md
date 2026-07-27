# 🛡️ GUÍA DE INSTALACIÓN RÁPIDA - AEGIS PRIME MASTER SOC
**Autor:** Eduardo Mex Rodriguez (EMR) (Defensive Security Engineering Portfolio)

¡Gracias por adquirir la suite de ciberseguridad defensiva **Aegis Prime Master SOC**!

---

## 📋 1. Requisitos Previos del Sistema
- **Sistema Operativo:** Linux (Ubuntu / Debian / Kali) o Windows 10/11 con PowerShell.
- **Python:** Versión 3.10 o superior (Verificar con `python --version`).
- **Librerías requeridas:** `flask`, `requests` (Instalar con `pip install flask requests`).

---

## 🚀 2. Instrucciones de Ejecución Paso a Paso

### 🔴 Paso A: Iniciar el Centro de Mando SOC Máster (Plataforma Principal)
Abre tu terminal o PowerShell en la carpeta del proyecto y ejecuta:
```bash
python core/aegis_master_engine.py
```
*Esto iniciará la orquestación de todos los módulos defensivos y el panel visual.*

### 🟢 Paso B: Iniciar el Bot SOAR Interactivo de Telegram (Notificaciones Móviles)
Para recibir alertas en tiempo real en tu celular con botones interactivos de bloqueo:
```bash
python bot/interactive_soar_bot.py TU_TELEGRAM_BOT_TOKEN TU_TELEGRAM_CHAT_ID
```

### 🟡 Paso C: Visualizar el Panel de Control 3D (Command Center)
Abre en cualquier navegador web (Chrome, Brave, Firefox) la siguiente ruta:
`dashboard/aegis_master_command_center.html`

---

## 🛠️ 3. Módulos Adicionales Incluidos

1. **Anti-Ransomware & Copia Cifrada:**
   `python modules/anti_ransomware_vault.py`
2. **Enrutador de Alertas Multicanal:**
   `python modules/multichannel_alert_router.py`
3. **Generador de Certificado de Cumplimiento ISO 27001 / NIST:**
   `python modules/generate_compliance_certificate.py`

---

## 📞 4. Licencia y Soporte
- **Licencia:** Protegido bajo Licencia MIT a nombre de **EMR**.
- Para dudas o soporte técnico, contacta a través de la plataforma de compra.
