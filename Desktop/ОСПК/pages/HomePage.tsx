import { useState, useEffect } from "react";
import { Navigation } from "../Navigation";
import { HeroSection } from "../HeroSection";
import { AboutSection } from "../AboutSection";
import { MembershipSection } from "../MembershipSection";
import { TeamSection } from "../TeamSection";
import { DocumentsSection } from "../DocumentsSection";
import { NewsSection } from "../NewsSection";
import { GallerySection } from "../GallerySection";
import { ContactsSection } from "../ContactsSection";
import { Footer } from "../Footer";
import { ScrollToTop } from "../ScrollToTop";

export function HomePage() {
  const [activeSection, setActiveSection] = useState("home");

  useEffect(() => {
    const handleScroll = () => {
      const sections = [
        "home",
        "about",
        "membership",
        "team",
        "documents",
        "news",
        "gallery",
        "contacts",
      ];
      
      for (const section of sections) {
        const element = document.getElementById(section);
        if (element) {
          const rect = element.getBoundingClientRect();
          if (rect.top <= 100 && rect.bottom >= 100) {
            setActiveSection(section);
            break;
          }
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Navigation activeSection={activeSection} onNavigate={scrollToSection} />
      <ScrollToTop />
      
      <main>
        <div id="home">
          <HeroSection />
        </div>
        
        <div id="about">
          <AboutSection />
        </div>
        
        <div id="membership">
          <MembershipSection />
        </div>
        
        <div id="team">
          <TeamSection />
        </div>
        
        <div id="documents">
          <DocumentsSection />
        </div>
        
        <div id="news">
          <NewsSection />
        </div>
        
        <div id="gallery">
          <GallerySection />
        </div>
        
        <div id="contacts">
          <ContactsSection />
        </div>
      </main>

      <Footer />
    </div>
  );
}

