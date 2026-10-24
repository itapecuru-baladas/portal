useEffect(() => {
  async function fetchNoticias() {
    setLoading(true);
    try {
      const res = await fetch('/api/noticias');
      const data = await res.json();
      if (Array.isArray(data)) {
        const unicas = Array.from(new Map(data.map((n:any) => [n.link, n])).values()) as Noticia[];
        const filtradas = active === "Todos" ? unicas : unicas.filter(n => (n.categoria||"").toLowerCase().includes(active.toLowerCase()));
        setNoticias(filtradas);
      }
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  }
  fetchNoticias();
}, [active]);