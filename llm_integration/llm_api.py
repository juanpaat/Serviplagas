"""
Módulo para integración real con APIs de LLM.
Este módulo será utilizado cuando se tengan las claves API correspondientes.
"""

import os
from typing import Optional
from config.settings import LLM_CONFIG, API_KEYS


class LLMAPIIntegration:
    """Integración real con APIs de LLM para análisis de datos."""
    
    def __init__(self):
        self.enabled = LLM_CONFIG['enabled']
        self.provider = LLM_CONFIG['provider']
        self.model = LLM_CONFIG['model']
        self.max_tokens = LLM_CONFIG['max_tokens']
        self.temperature = LLM_CONFIG['temperature']
        
        # Verificar si hay claves API disponibles
        self.api_key = self._get_api_key()
        
    def _get_api_key(self) -> Optional[str]:
        """Obtiene la clave API según el proveedor configurado."""
        if self.provider == 'openai':
            return API_KEYS['openai'] or os.getenv('OPENAI_API_KEY')
        elif self.provider == 'anthropic':
            return API_KEYS['anthropic'] or os.getenv('ANTHROPIC_API_KEY')
        return None
    
    def is_available(self) -> bool:
        """Verifica si la integración LLM está disponible."""
        return self.enabled and self.api_key is not None
    
    def analyze_table(self, prompt: str) -> str:
        """
        Analiza una tabla usando el LLM configurado.
        
        Args:
            prompt: El prompt con la tabla y las instrucciones
            
        Returns:
            str: Análisis generado por el LLM
        """
        if not self.is_available():
            return self._fallback_analysis(prompt)
        
        try:
            if self.provider == 'openai':
                return self._call_openai(prompt)
            elif self.provider == 'anthropic':
                return self._call_anthropic(prompt)
            else:
                return self._fallback_analysis(prompt)
                
        except Exception as e:
            print(f"❌ Error llamando a LLM: {e}")
            return self._fallback_analysis(prompt)
    
    def _call_openai(self, prompt: str) -> str:
        """Llama a la API de OpenAI."""
        try:
            import openai
            
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto analista de datos de control de plagas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            print("⚠️  Biblioteca openai no instalada. Instalar con: pip install openai")
            return self._fallback_analysis(prompt)
        except Exception as e:
            print(f"❌ Error en API OpenAI: {e}")
            return self._fallback_analysis(prompt)
    
    def _call_anthropic(self, prompt: str) -> str:
        """Llama a la API de Anthropic (Claude)."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except ImportError:
            print("⚠️  Biblioteca anthropic no instalada. Instalar con: pip install anthropic")
            return self._fallback_analysis(prompt)
        except Exception as e:
            print(f"❌ Error en API Anthropic: {e}")
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        """Análisis de fallback cuando no hay LLM disponible."""
        return """
        [ANÁLISIS AUTOMÁTICO - LLM NO DISPONIBLE]
        
        Los datos han sido procesados y están listos para análisis.
        Para obtener análisis detallados, configure una clave API de LLM en config/settings.py
        o como variable de entorno.
        
        Configuración actual:
        - LLM habilitado: {enabled}
        - Proveedor: {provider}
        - API Key disponible: {api_available}
        
        Para habilitar análisis LLM:
        1. Obtener clave API de OpenAI o Anthropic
        2. Configurar en config/settings.py o como variable de entorno
        3. Cambiar LLM_CONFIG['enabled'] = True
        """.format(
            enabled=self.enabled,
            provider=self.provider,
            api_available=bool(self.api_key)
        )


def get_llm_analysis(prompt: str) -> str:
    """
    Función de conveniencia para obtener análisis LLM.
    
    Args:
        prompt: El prompt a analizar
        
    Returns:
        str: Análisis del LLM o mensaje de fallback
    """
    llm = LLMAPIIntegration()
    return llm.analyze_table(prompt)
