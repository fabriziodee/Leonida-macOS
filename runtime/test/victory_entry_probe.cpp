#include <windows.h>

extern "C" DWORD WINAPI probe_entry() {
    constexpr char message[] = "VIctory synthetic title entry reached\r\n";
    DWORD written = 0;
    if (!WriteFile(GetStdHandle(STD_OUTPUT_HANDLE), message, sizeof(message) - 1, &written, nullptr)) {
        return 41;
    }
    return written == sizeof(message) - 1 ? 42 : 43;
}
