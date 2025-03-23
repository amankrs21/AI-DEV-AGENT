import { useState, useEffect } from 'react';


// Typewriter effect component
const TypewriterEffect = ({ strings, delay = 50, deleteSpeed = 20 }) => {
    const [currentText, setCurrentText] = useState('\u00A0');
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isDeleting, setIsDeleting] = useState(false);
    const [charIndex, setCharIndex] = useState(0);

    useEffect(() => {
        const type = () => {
            const fullText = strings[currentIndex % strings.length];
            if (!isDeleting && charIndex < fullText.length) {
                setCurrentText(fullText.substring(0, charIndex + 1));
                setCharIndex(charIndex + 1);
            } else if (isDeleting && charIndex > 0) {
                setCurrentText(fullText.substring(0, charIndex - 1) || '\u00A0');
                setCharIndex(charIndex - 1);
            } else if (!isDeleting && charIndex === fullText.length) {
                setTimeout(() => setIsDeleting(true), 1000);
            } else if (isDeleting && charIndex === 0) {
                setIsDeleting(false);
                setCurrentIndex(currentIndex + 1);
            }
        };

        const speed = isDeleting ? deleteSpeed : delay;
        const timer = setTimeout(type, speed);
        return () => clearTimeout(timer);
    }, [charIndex, isDeleting, currentIndex, strings, delay, deleteSpeed]);

    return <span dangerouslySetInnerHTML={{ __html: currentText }} />;
};

export default TypewriterEffect;