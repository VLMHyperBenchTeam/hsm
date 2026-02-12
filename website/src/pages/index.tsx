import React, {useEffect} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {useColorMode} from '@docusaurus/theme-common';
import useIsBrowser from '@docusaurus/useIsBrowser';
import NeuralBackground from '@site/src/components/NeuralBackground';
import Mermaid from '@theme/Mermaid';

function HomeContent(): React.JSX.Element {
  const isBrowser = useIsBrowser();
  const {setColorMode} = useColorMode();

  useEffect(() => {
    if (isBrowser) {
      setColorMode('dark');
      document.documentElement.classList.add('home-page-active');
    }
    return () => {
      if (isBrowser) {
        document.documentElement.classList.remove('home-page-active');
      }
    };
  }, [isBrowser, setColorMode]);

  return (
    <>
      <NeuralBackground />
      
      <div className="relative z-40 w-full min-h-screen flex flex-col items-center justify-center p-4 md:p-12 pt-32 md:pt-48">
        
        {/* Main Title Section */}
        <div className="text-center mb-24 relative">
          <h1 className="font-display text-5xl md:text-7xl font-bold text-white tracking-tight mb-8 neon-text-cyan">
            HYPER STACK <span className="text-secondary neon-text-lime">MANAGER</span>
          </h1>
          <p className="font-mono text-slate-300 text-lg md:text-xl tracking-widest uppercase opacity-80 leading-relaxed">
            Гипервизор окружений для современных гибридных стеков
          </p>
          
          {/* Quick Start Button */}
          <div className="mt-14 md:mt-16 flex justify-center quick-start-button-container">
            <Link
              to="/docs/intro"
              className="group relative inline-flex items-center justify-center px-8 py-4 font-display font-bold border-2 transition-all duration-300 no-underline quick-start-button-fixed"
              style={{
                clipPath: 'polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px)'
              }}
            >
              <span className="mr-3 text-lg font-mono">
                {'>'}<span className="terminal-cursor">_</span>
              </span>
              <span className="tracking-[0.2em]">БЫСТРЫЙ СТАРТ - 5 МИН</span>
              
              {/* Decorative corner arrow */}
              <svg className="absolute -bottom-1 -right-1 w-4 h-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:translate-x-1 group-hover:translate-y-1"
                   style={{ color: '#00FFCC' }}
                   viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M7 17L17 17L17 7" />
              </svg>
            </Link>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-7xl px-4">
          
          {/* Card 1: Lego Architecture */}
          <div className="group relative bg-[#0e1116]/10 backdrop-blur-sm border border-primary/10 p-8 hover:border-primary/40 transition-all duration-500 hover:bg-[#0e1116]/30 hover:shadow-[0_0_30px_rgba(0,255,204,0.05)]"
               style={{
                 clipPath: 'polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px)'
               }}>
            {/* Top decorative line */}
            <div className="absolute top-0 left-0 w-20 h-[1px] bg-primary/30"></div>
            <div className="absolute top-0 left-0 w-[1px] h-4 bg-primary/30"></div>
            
            {/* Top right dots */}
            <div className="absolute top-3 right-3 flex gap-1 opacity-40">
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
            </div>
            
            <div className="mb-6 text-primary">
              <span className="material-symbols-outlined text-5xl drop-shadow-[0_0_10px_rgba(0,255,204,0.5)]">deployed_code</span>
            </div>
            
            <h3 className="font-display text-xl md:text-2xl font-bold text-secondary mb-4 uppercase tracking-wide">
              Lego-архитектура
            </h3>
            
            <p className="font-mono text-base md:text-lg text-slate-400 leading-relaxed">
              Собирайте свой стек из независимых компонентов. Легко подменяйте реализации интерфейсов (например, одну векторную БД на другую) одной командой.
            </p>
          </div>

          {/* Card 2: Hybrid Orchestration */}
          <div className="group relative bg-[#0e1116]/10 backdrop-blur-sm border border-primary/10 p-8 hover:border-primary/40 transition-all duration-500 hover:bg-[#0e1116]/30 hover:shadow-[0_0_30px_rgba(0,255,204,0.05)]"
               style={{
                 clipPath: 'polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px)'
               }}>
            {/* Top decorative line */}
            <div className="absolute top-0 left-0 w-20 h-[1px] bg-primary/30"></div>
            <div className="absolute top-0 left-0 w-[1px] h-4 bg-primary/30"></div>

            {/* Top right dots */}
            <div className="absolute top-3 right-3 flex gap-1 opacity-40">
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
            </div>

            <div className="mb-6 text-primary">
              <span className="material-symbols-outlined text-5xl drop-shadow-[0_0_10px_rgba(0,255,204,0.5)]">dns</span>
            </div>
            
            <h3 className="font-display text-xl md:text-2xl font-bold text-secondary mb-4 uppercase tracking-wide">
              Гибридная оркестрация
            </h3>
            
            <p className="font-mono text-base md:text-lg text-slate-400 leading-relaxed">
              Единое управление Python-пакетами (через uv) и инфраструктурными сервисами (через docker compose) в одном манифесте.
            </p>
          </div>

          {/* Card 3: Atomic Synchronization */}
          <div className="group relative bg-[#0e1116]/10 backdrop-blur-sm border border-primary/10 p-8 hover:border-primary/40 transition-all duration-500 hover:bg-[#0e1116]/30 hover:shadow-[0_0_30px_rgba(0,255,204,0.05)]"
               style={{
                 clipPath: 'polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px)'
               }}>
            {/* Top decorative line */}
            <div className="absolute top-0 left-0 w-20 h-[1px] bg-primary/30"></div>
            <div className="absolute top-0 left-0 w-[1px] h-4 bg-primary/30"></div>

            {/* Top right dots */}
            <div className="absolute top-3 right-3 flex gap-1 opacity-40">
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
            </div>

            <div className="mb-6 text-primary">
              <span className="material-symbols-outlined text-5xl drop-shadow-[0_0_10px_rgba(0,255,204,0.5)]">sync_lock</span>
            </div>
            
            <h3 className="font-display text-xl md:text-2xl font-bold text-secondary mb-4 uppercase tracking-wide">
              Атомарная синхронизация
            </h3>
            
            <p className="font-mono text-base md:text-lg text-slate-400 leading-relaxed">
              Транзакционное обновление конфигураций. Если зависимости не разрешаются, ваши рабочие файлы остаются в стабильном состоянии.
            </p>
          </div>

        </div>

        {/* Organic Content Sections */}
        <div className="relative z-40 w-full max-w-7xl mx-auto px-4 py-24 space-y-32 font-mono text-slate-300">
          
          {/* Section: About */}
          <section className="relative">
            <div className="absolute -left-4 top-0 w-1 h-full bg-gradient-to-b from-primary to-transparent opacity-20"></div>
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-8 uppercase tracking-wider neon-text-cyan">
              О проекте <span className="text-white">HYPER STACK</span> <span className="text-secondary">MANAGER</span> <span className="text-white">(HSM)</span>
            </h2>
            <div className="space-y-6">
              <blockquote className="border-l-4 border-secondary bg-secondary/5 p-6 italic text-secondary text-lg md:text-xl leading-relaxed">
                Объедините Python-пакеты и сервисы (Docker и uv venv) в единую, управляемую экосистему.
              </blockquote>
              <p className="text-base md:text-lg">
                В HSM всё строится вокруг понятия <span className="text-secondary font-bold">Компонента</span>.
              </p>
              <blockquote className="border-l-4 border-primary bg-primary/5 p-6 italic text-lg md:text-xl leading-relaxed">
                <strong>Компонент</strong> — это отдельный Git-репозиторий, который может быть Python-пакетом или сервисом (Docker и uv venv).
              </blockquote>
              <p className="text-base md:text-lg">
                Реестр хранит данные о компонентах, позволяя собирать проект из них как конструктор.
              </p>
            </div>
          </section>

          <hr className="border-primary/10" />

          {/* Section: Why HSM */}
          <section className="space-y-12">
            <div className="text-center max-w-3xl mx-auto">
              <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-6 uppercase tracking-wider neon-text-cyan">
                Зачем это нужно?
              </h2>
              <p className="text-base md:text-lg text-slate-400 leading-relaxed">
                Разработка современных многокомпонентных систем — это хаос из разрозненных инструментов.
                Вы правите код в одном месте, конфиги сервисов в другом, а переменные окружения — в третьем.
              </p>
            </div>

            <div className="space-y-32">
              {/* Before */}
              <div className="space-y-12">
                <h3 className="font-display text-2xl md:text-3xl font-bold text-red-400 uppercase tracking-tight border-b border-red-500/20 pb-4 text-center">
                  Раньше: Ручная синхронизация стека разработки
                </h3>
                <div className="bg-[#0e1116]/50 border border-red-500/10 p-8 rounded-xl">
                  <Mermaid value={`
graph TD
    Dev([Разработчик - ВЫ]) -- "ручная правка" --> Project
    Dev -- "ручная правка" --> Docker

    subgraph Project ["Проект - Main"]
        P1[pyproject.toml]
        PK1[python packages]
        E1[Project ENV]
    end

    subgraph Docker ["Инфраструктура - Docker"]
        direction TB
        DC[docker-compose.yml]
        DC --> S1
        DC --> S2
        
        subgraph S1 ["Сервис 1"]
            V1[volumes/ports]
            E2[Service 1 ENV]
        end

        subgraph S2 ["Сервис 2"]
            V2[volumes/ports]
            E3[Service 2 ENV]
        end
    end
                  `} />
                </div>
                <div className="max-w-4xl mx-auto space-y-8">
                  <p className="font-display text-xl font-bold text-red-400/80 uppercase tracking-widest text-center">Почему это неудобно?</p>
                  <ul className="list-none grid grid-cols-1 md:grid-cols-2 gap-6 p-0">
                    <li className="p-8 bg-red-500/5 border border-red-500/10 rounded-xl backdrop-blur-sm">
                      <p className="text-red-400 font-bold text-base md:text-lg uppercase mb-4 tracking-widest flex items-center gap-2">
                        <span>×</span> Ручная синхронизация (Manual Glue)
                      </p>
                      <p className="text-base md:text-lg text-slate-400 leading-relaxed">Вы — единственный "оркестратор". Вы вручную синхронизируете pyproject.toml, docker-compose.yml и .env. Ошибка в одной строке — и проект не запускается.</p>
                    </li>
                    <li className="p-8 bg-red-500/5 border border-red-500/10 rounded-xl backdrop-blur-sm">
                      <p className="text-red-400 font-bold text-base md:text-lg uppercase mb-4 tracking-widest flex items-center gap-2">
                        <span>×</span> Статичная инфраструктура
                      </p>
                      <p className="text-base md:text-lg text-slate-400 leading-relaxed">docker-compose.yml не знает о ваших намерениях. Переключение между prod и dev — это рутина с комментариями и правкой путей.</p>
                    </li>
                    <li className="p-8 bg-red-500/5 border border-red-500/10 rounded-xl backdrop-blur-sm">
                      <p className="text-red-400 font-bold text-base md:text-lg uppercase mb-4 tracking-widest flex items-center gap-2">
                        <span>×</span> Проблемы модульной разработки
                      </p>
                      <p className="text-base md:text-lg text-slate-400 leading-relaxed">Работа с вложенными Git-репозиториями вызывает трудности. uv workspaces требует жесткой структуры, а git submodules — ручного управления.</p>
                    </li>
                    <li className="p-8 bg-red-500/5 border border-red-500/10 rounded-xl backdrop-blur-sm">
                      <p className="text-red-400 font-bold text-base md:text-lg uppercase mb-4 tracking-widest flex items-center gap-2">
                        <span>×</span> Слепые зависимости
                      </p>
                      <p className="text-base md:text-lg text-slate-400 leading-relaxed">Вы добавляете библиотеку, но надеетесь, что не забыли поднять для неё базу. Зависимости живут только в вашей голове.</p>
                    </li>
                    <li className="p-8 bg-red-500/5 border border-red-500/10 rounded-xl backdrop-blur-sm">
                      <p className="text-red-400 font-bold text-base md:text-lg uppercase mb-4 tracking-widest flex items-center gap-2">
                        <span>×</span> Конфликты в Python-окружении
                      </p>
                      <p className="text-base md:text-lg text-slate-400 leading-relaxed">Попытка запустить два сервиса с разными версиями одной библиотеки в одном монорепозитории превращается в квест.</p>
                    </li>
                    <li className="p-8 bg-red-500/5 border border-red-500/10 rounded-xl backdrop-blur-sm">
                      <p className="text-red-400 font-bold text-base md:text-lg uppercase mb-4 tracking-widest flex items-center gap-2">
                        <span>×</span> Неатомарные правки
                      </p>
                      <p className="text-base md:text-lg text-slate-400 leading-relaxed">Ошибка установки оставляет проект в "полусломанном" состоянии. Откатывать изменения приходится вручную.</p>
                    </li>
                  </ul>
                </div>
              </div>

              {/* After */}
              <div className="space-y-12">
                <h3 className="font-display text-2xl md:text-3xl font-bold text-primary uppercase tracking-tight border-b border-primary/20 pb-4 text-center">
                  С HSM: Декларативное единство
                </h3>
                <div className="bg-[#0e1116]/50 border border-primary/10 p-8 rounded-xl shadow-[0_0_50px_rgba(0,255,204,0.05)]">
                  <Mermaid value={`
graph TD
    Manifest[hsm.yaml] -- "дирижирует" --> HSM[HSM Engine]
    
    HSM --> Project
    HSM --> Docker
    HSM --> S3

    subgraph Project ["Проект - Main"]
        P2[pyproject.toml]
        PK2[python packages]
        E2[Project ENV]
    end

    subgraph Docker ["Инфраструктура - Docker"]
        direction TB
        DCH[docker-compose.hsm.yml]
        DCH --> S1
        DCH --> S2

        subgraph S1 ["Сервис 1"]
            V3[volumes/ports]
            E3[Service 1 ENV]
        end

        subgraph S2 ["Сервис 2"]
            V4[volumes/ports]
            E4[Service 2 ENV]
        end
    end

    subgraph S3 ["Сервис 3 - UV"]
        V5[uv venv]
        PK3[python packages]
        E5[Service 3 ENV]
    end
                  `} />
                </div>
                <div className="max-w-4xl mx-auto space-y-12">
                  <div className="space-y-6">
                    <h4 className="font-display text-xl md:text-2xl font-bold text-primary uppercase tracking-widest flex items-center gap-3">
                      <span className="text-2xl">🧩</span> Динамический "Виртуальный Монорепозиторий"
                    </h4>
                    <p className="text-base md:text-lg leading-relaxed">HSM позволяет работать с распределенной системой как с единым целым:</p>
                    <ul className="list-none space-y-4 p-0 pl-8">
                      <li className="relative before:content-['•'] before:absolute before:-left-6 before:text-primary text-base md:text-lg">
                        <strong>Чистота Polyrepo</strong>: Каждый компонент сохраняет свою историю и независимость.
                      </li>
                      <li className="relative before:content-['•'] before:absolute before:-left-6 before:text-primary text-base md:text-lg">
                        <strong>Удобство Monorepo</strong>: В режиме <code className="text-primary">dev</code> HSM материализует нужные компоненты в единое рабочее пространство.
                      </li>
                      <li className="relative before:content-['•'] before:absolute before:-left-6 before:text-primary text-base md:text-lg">
                        <strong>Инфраструктура, следующая за кодом</strong>: Ваше окружение — это не только файлы, но и живые сервисы с автоматической оркестрацией, Hot-Reload и пробросом ENV-контекста.
                      </li>
                    </ul>
                  </div>

                  <div className="space-y-6">
                    <h4 className="font-display text-xl md:text-2xl font-bold text-primary uppercase tracking-widest flex items-center gap-3">
                      <span className="text-2xl">⚡️</span> Покомпонентный контроль (Granular Control)
                    </h4>
                    <p className="text-base md:text-lg leading-relaxed">Вы управляете состоянием каждого компонента отдельно:</p>
                    <ul className="list-none space-y-4 p-0 pl-8">
                      <li className="relative before:content-['•'] before:absolute before:-left-6 before:text-primary text-base md:text-lg">
                        <strong>Режим <code className="text-primary">prod</code></strong>: Использование стабильных версий (пакеты из Git/PyPI или готовые Docker-образы).
                      </li>
                      <li className="relative before:content-['•'] before:absolute before:-left-6 before:text-primary text-base md:text-lg">
                        <strong>Режим <code className="text-primary">dev</code></strong>: Переключение компонента на <strong>локальные исходники</strong> (editable install или <code className="text-primary">build</code> контекст).
                      </li>
                      <li className="relative before:content-['•'] before:absolute before:-left-6 before:text-primary text-base md:text-lg">
                        <strong>Смешанный стек</strong>: Можно держать весь проект в <code className="text-primary">prod</code>, но одну библиотеку, в которой правите баг, переключить в <code className="text-primary">dev</code>.
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section: Implies */}
          <section className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h2 className="font-display text-3xl md:text-4xl font-bold text-white uppercase tracking-wider neon-text-cyan">
                🧠 Умные зависимости (Implies)
              </h2>
              <p className="text-base md:text-lg leading-relaxed">
                Выбранные Python-пакеты умеют "заказывать" инфраструктуру. Если вы добавляете библиотеку <code className="text-primary">auth-plugin</code>, HSM сам поймет, что ей нужен сервис <code className="text-primary">postgres</code>, добавит его в стек и настроит доступы.
                И наоборот, выбранный сервис может заказать Python-пакет.
              </p>
              <p className="text-base md:text-lg text-secondary font-bold italic leading-relaxed">
                Вы описываете Намерение через CLI-команды (что вы хотите), HSM берет на себя Реализацию (как это настроить).
              </p>
            </div>
            <div className="bg-[#0e1116]/50 border border-primary/20 p-6 rounded-lg">
              <Mermaid value={`
graph TD
    CLI[> hsm library mode qdrant-client dev] --> HSM_YAML[Обновляет hsm.yaml]
    HSM_YAML -- "hsm sync" --> HSM_Engine[HSM Engine: Реализует]
    
    HSM_Engine -- "add qdrant-client" --> Project
    HSM_Engine -- "запуск Сервис 1 Qdrant (Docker)" --> S1

    subgraph Project ["Проект (Main)"]
        P2[pyproject.toml]
        PK2[python packages<br/>Editable install]
        E2[Project ENV]
    end

    subgraph S1 ["Сервис 1 Qdrant (Docker)"]
        D2[docker-compose.hsm.yml]
        V3[volumes/ports<br/>Hot-Reload]
        E3[Service ENV]
    end
              `} />
            </div>
          </section>

          {/* Section: Atomic Sync & Visual Proof */}
          <section className="space-y-12">
            <div className="bg-secondary/5 border border-secondary/20 p-6 rounded-lg text-center">
              <h3 className="text-secondary font-bold uppercase tracking-widest mb-2">🛡️ Атомарная синхронизация</h3>
              <p className="text-base md:text-lg leading-relaxed">Синхронизация — это транзакция. Если зависимости не сошлись, HSM откатит изменения в конфигах.</p>
            </div>

            <div className="max-w-4xl mx-auto">
              <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-8 text-center uppercase tracking-widest">
                🚀 Посмотрите в деле (Visual Proof)
              </h2>
              <div className="bg-[#0e1116] border border-primary/30 rounded-lg overflow-hidden shadow-2xl">
                <div className="bg-[#1e1e1e] px-4 py-2 border-b border-primary/10 flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                  <span className="ml-4 font-mono text-xs text-slate-500 uppercase tracking-widest">Terminal — hsm sync</span>
                </div>
                <div className="p-8 font-mono text-sm leading-relaxed">
                  <div className="flex gap-3 mb-2">
                    <span className="text-primary">$</span>
                    <span className="text-slate-300">hsm service mode auth-service dev</span>
                  </div>
                  <div className="text-slate-500 mb-6"># 1. Переключаем сервис в режим разработки</div>
                  <div className="flex gap-3 mb-2">
                    <span className="text-primary">$</span>
                    <span className="text-slate-300">hsm sync</span>
                  </div>
                  <div className="text-slate-500 mb-4"># 2. Синхронизируем стек</div>
                  <div className="space-y-1 text-primary/80">
                    <p>› Finding auth-service in Registry... [OK]</p>
                    <p>› Generating docker-compose.hsm.yml... [OK]</p>
                    <p>› Injecting ENV variables... [OK]</p>
                    <p>› Restarting container with local volumes... [OK]</p>
                  </div>
                  <div className="mt-6 p-4 bg-primary/10 border border-primary/20 text-primary font-bold rounded">
                    SUCCESS: Стек синхронизирован. Вы правите код — изменения мгновенно подхватываются в контейнере.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section: Anatomy */}
          <section className="space-y-8">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white uppercase tracking-wider neon-text-cyan">
              📦 Анатомия проекта
            </h2>
            <ul className="space-y-6 list-none p-0">
              <li>
                <span className="text-primary font-bold block mb-1 uppercase text-base md:text-lg tracking-widest">hsm.yaml</span>
                <p className="text-base md:text-lg">Манифест вашего проекта. Single Source of Truth, который можно править вручную или через CLI.</p>
              </li>
              <li>
                <span className="text-primary font-bold block mb-1 uppercase text-base md:text-lg tracking-widest">Реестр (Registry)</span>
                <p className="text-base md:text-lg">База знаний о компонентах. Описывает, откуда брать код и как запускать сервисы.</p>
              </li>
              <li>
                <span className="text-primary font-bold block mb-1 uppercase text-base md:text-lg tracking-widest">Адаптеры</span>
                <p className="text-base md:text-lg">Модули-исполнители, которые транслируют ваши желания в команды для uv, docker, pixi и др.</p>
              </li>
            </ul>
          </section>

          {/* Section: Registry */}
          <section className="space-y-8">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white uppercase tracking-wider neon-text-cyan">
              📚 Реестр: База знаний вашего стека
            </h2>
            <p className="text-base md:text-lg text-slate-400 leading-relaxed">
              Реестр — это не просто список зависимостей, это <strong>интеллект вашего проекта</strong>. Настройте его один раз и переиспользуйте между командами и проектами.
            </p>
            <div className="bg-[#0e1116]/50 border border-primary/20 p-8 rounded-lg">
              <Mermaid value={`
graph TD
    Registry[(HSM Registry)]
    
    Registry --> Libs[Python Библиотеки]
    Registry --> Svcs[Автономные Сервисы]
    Registry --> Groups[Группы выбора / Интерфейсы]

    subgraph "Типы компонентов"
        Libs --> L1[auth-lib]
        Libs --> L2[core-utils]
        
        Svcs --> S1[Postgres<br/>Docker runtime]
        Svcs --> S2[ML-Worker<br/>uv venv runtime]
    end

    subgraph "Умный выбор"
        Groups --> G1[Vector DB<br/>1-of-N]
        Groups --> G2[Monitoring<br/>M-of-N]
        
        G1 -.-> Qdrant
        G1 -.-> Milvus
    end
              `} />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
              <div className="p-8 bg-primary/5 border border-primary/10 rounded-xl backdrop-blur-sm hover:border-primary/30 transition-colors">
                <p className="text-primary font-bold text-lg md:text-xl uppercase mb-3 tracking-widest">Python-пакеты</p>
                <p className="text-base md:text-lg text-slate-400 leading-relaxed">Описание источников (Git/PyPI/Local) и зависимостей. Полная поддержка editable-режима.</p>
              </div>
              <div className="p-8 bg-primary/5 border border-primary/10 rounded-xl backdrop-blur-sm hover:border-primary/30 transition-colors">
                <p className="text-primary font-bold text-lg md:text-xl uppercase mb-3 tracking-widest">Docker-сервисы</p>
                <p className="text-base md:text-lg text-slate-400 leading-relaxed">Готовые образы или локальные репозитории для сборки с автоматическим пробросом томов.</p>
              </div>
              <div className="p-8 bg-primary/5 border border-primary/10 rounded-xl backdrop-blur-sm hover:border-primary/30 transition-colors">
                <p className="text-primary font-bold text-lg md:text-xl uppercase mb-3 tracking-widest">uv venv (VES)</p>
                <p className="text-base md:text-lg text-slate-400 leading-relaxed">Полностью изолированные Python-сервисы со своими lock-файлами через Virtual Environment Services.</p>
              </div>
              <div className="p-8 bg-primary/5 border border-primary/10 rounded-xl backdrop-blur-sm hover:border-primary/30 transition-colors">
                <p className="text-primary font-bold text-lg md:text-xl uppercase mb-3 tracking-widest">Группы (Интерфейсы)</p>
                <p className="text-base md:text-lg text-slate-400 leading-relaxed">Абстрагируйтесь от реализаций. Выбирайте "Векторную БД", а не конкретный конфиг.</p>
              </div>
            </div>
          </section>

          {/* Section: Comparison Table */}
          <section className="max-w-4xl mx-auto overflow-x-auto">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-12 text-center uppercase tracking-wider neon-text-cyan">
              🎯 Коротко о главном
            </h2>
            <table className="w-full border-collapse border border-primary/20 font-mono text-base md:text-lg">
              <thead>
                <tr className="bg-primary/10">
                  <th className="border border-primary/20 p-4 text-primary text-left uppercase tracking-widest">✅ HSM — это</th>
                  <th className="border border-primary/20 p-4 text-slate-500 text-left uppercase tracking-widest">❌ HSM — это НЕ</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-primary/20 p-4"><strong>Мета-оркестратор</strong>: Дирижер для uv, docker и git.</td>
                  <td className="border border-primary/20 p-4 text-slate-500"><strong>НЕ замена uv или docker</strong>: Он использует их мощь.</td>
                </tr>
                <tr>
                  <td className="border border-primary/20 p-4"><strong>Гипервизор окружений</strong>: Абстракция над стеком.</td>
                  <td className="border border-primary/20 p-4 text-slate-500"><strong>НЕ система сборки</strong>: Он не заменяет make или hatch.</td>
                </tr>
                <tr>
                  <td className="border border-primary/20 p-4"><strong>Инструмент для DX</strong>: Убирает рутину.</td>
                  <td className="border border-primary/20 p-4 text-slate-500"><strong>НЕ замена Git</strong>: Он автоматизирует работу с ним.</td>
                </tr>
              </tbody>
            </table>
          </section>

          {/* Section: Quick Start Final */}
          <section className="text-center space-y-12 py-12">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white uppercase tracking-widest neon-text-cyan">
              🏁 Быстрый старт
            </h2>
            <div className="max-w-2xl mx-auto bg-[#0e1116] border border-primary/30 p-8 rounded-2xl shadow-[0_0_50px_rgba(0,255,204,0.1)]">
              <div className="space-y-6 text-left font-mono">
                <div>
                  <p className="text-slate-500 text-sm mb-2 uppercase tracking-widest"># 1. Установка</p>
                  <code className="text-primary block bg-black/40 p-4 rounded border border-primary/10 text-base">uv tool install git+https://github.com/VLMHyperBenchTeam/hsm.git</code>
                </div>
                <div>
                  <p className="text-slate-500 text-sm mb-2 uppercase tracking-widest"># 2. Инициализация</p>
                  <code className="text-primary block bg-black/40 p-4 rounded border border-primary/10 text-base">hsm init</code>
                </div>
                <div>
                  <p className="text-slate-500 text-sm mb-2 uppercase tracking-widest"># 3. Добавление компонента</p>
                  <code className="text-primary block bg-black/40 p-4 rounded border border-primary/10 text-base">hsm library add my-cool-lib</code>
                </div>
                <div>
                  <p className="text-slate-500 text-sm mb-2 uppercase tracking-widest"># 4. Синхронизация</p>
                  <code className="text-primary block bg-black/40 p-4 rounded border border-primary/10 text-base">hsm sync</code>
                </div>
              </div>
              <div className="mt-12">
                <Link to="/docs/intro" className="inline-block bg-primary text-black px-12 py-4 rounded-lg font-display font-bold uppercase tracking-[0.2em] hover:bg-white transition-all hover:shadow-[0_0_20px_#00FFCC]">
                  Пройти вводный туториал
                </Link>
                <p className="mt-4 text-slate-500 text-xs uppercase tracking-widest">(120 секунд)</p>
              </div>
            </div>
          </section>

          {/* Section: Final Call to Action */}
          <section className="text-center space-y-8 pb-24">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white uppercase tracking-widest">
              🏁 Готовы объединить Python и сервисы?
            </h2>
            <p className="text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
              Не тратьте свое время на ручную синхронизацию конфигов. Позвольте HSM сделать это для вас.
            </p>
          </section>

        </div>

        {/* Footer Status Bar */}
        <div className="fixed bottom-0 left-0 right-0 h-8 bg-[#0e1116] border-t border-[#1e1e1e] flex items-center justify-between px-6 z-50">
          <div className="flex items-center gap-6 text-xs font-mono text-slate-500">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
              <span className="text-primary/80">ДОКУМЕНТАЦИЯ: СИНХРОНИЗИРОВАНА | v0.0.1</span>
            </div>
          </div>
          
          <div className="flex items-center gap-4 text-xs font-mono text-slate-500">
            <span className="hidden md:inline">Copyright © 2026 HyperTeam</span>
            <span className="text-secondary">СТАТУС_СИСТЕМЫ: ГОТОВА</span>
          </div>
        </div>

      </div>
    </>
  );
}

export default function Home(): React.JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  
  return (
    <Layout
      title={siteConfig.title}
      description={siteConfig.tagline}
      noFooter={true}
      wrapperClassName="home-page">
      <HomeContent />
    </Layout>
  );
}
