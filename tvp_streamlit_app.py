import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Copy, Sparkles, Phone, MessageSquare, Brain, ChevronRight, RefreshCcw } from "lucide-react";

const responseLibrary = {
  discovery: {
    label: "Discovery",
    objective: "Open the client up and learn what matters emotionally.",
    triggers: {
      just_looking: {
        label: "Just looking / not sure what I want",
        clientCue: "I'm just looking. I'm not totally sure what I want yet.",
        response:
          "Absolutely—and honestly, that’s the perfect place to start. Most of my clients don’t come in with a clear plan… they just know they want something meaningful. That’s really where I step in—helping you shape what this could look like in a way that feels natural and personal to you. Can I ask—what made you start thinking about doing this now?",
      },
      overwhelmed: {
        label: "Overwhelmed",
        clientCue: "I feel a little overwhelmed trying to figure it all out.",
        response:
          "That makes complete sense—and you’re not alone in that. This is actually why I’ve structured the experience the way I have… so you’re not trying to piece it all together on your own. I guide you through everything—from styling to how it all comes together—so it feels calm and fully taken care of. What part feels the most overwhelming right now?",
      },
      meaningful: {
        label: "Wants something meaningful",
        clientCue: "I want this to feel meaningful, not just like another photo session.",
        response:
          "I love that you said that—because that’s exactly the heart of what I do. This isn’t about just taking photos… it’s about creating something that reflects this moment in your life in a way that lasts. When you picture this a year from now… what would you want it to feel like when you see it?",
      },
    },
  },
  desire: {
    label: "Emotional Desire",
    objective: "Deepen emotional motivation and future vision.",
    triggers: {
      child_growing: {
        label: "Child is growing fast",
        clientCue: "She’s growing so fast and I don’t want to miss this stage.",
        response:
          "That stage goes by so quickly… and it’s one of the biggest reasons clients come to me. They’re not just trying to capture how things look—they’re trying to hold onto how it feels right now. That’s really what we design together.",
      },
      mother_daughter: {
        label: "Mother-daughter connection",
        clientCue: "I really want something special of the two of us.",
        response:
          "There’s something so meaningful about preserving that connection while you’re in it—not years after it’s changed. My goal is to create something that lets you feel this season again every time you see it.",
      },
    },
  },
  trust: {
    label: "Trust / Safety",
    objective: "Reduce fear and increase emotional safety.",
    triggers: {
      what_to_wear: {
        label: "Doesn’t know what to wear / how it works",
        clientCue: "I wouldn’t even know what to wear or how any of this works.",
        response:
          "That’s completely taken care of. You’re guided through everything—from wardrobe to posing—so you’re never left guessing. My role is to make sure you feel comfortable, confident, and fully supported the entire time.",
      },
      nervous_look: {
        label: "Nervous about how she will look",
        clientCue: "I’m nervous I won’t look good in pictures.",
        response:
          "I hear that a lot—and it’s a very real concern. The way I photograph and guide you is very intentional… so you’re not just standing there hoping for a good image. I’m shaping everything—light, pose, expression—to bring out the most natural and flattering version of you.",
      },
    },
  },
  objection: {
    label: "Objection",
    objective: "Interrupt the old pattern, differentiate, and solve the real fear.",
    triggers: {
      past_experience: {
        label: "Past bad experience / photos sat on phone",
        clientCue: "I’ve done photos before and then they just sat on my phone.",
        response:
          "I’m really glad you shared that—because that’s exactly what I’ve built this experience to avoid. Most photography sessions end with a gallery… and then you’re left trying to figure out what to do with it. What I do is very different. We design your artwork from the beginning—so before you even step into the session, we already know what this is going to become. So you’re not walking away with files… you’re walking away with something finished, meaningful, and part of your home. If it helps, I can show you what that would look like for you specifically.",
      },
      price: {
        label: "Price hesitation",
        clientCue: "I just don’t know if I can justify the investment.",
        response:
          "I completely understand—and honestly, most clients feel that way at first. This is an investment, and it should feel intentional. What I’ve found is that once they understand what they’re actually receiving—not just images, but finished artwork—they feel very differently about it. This isn’t something that ends up in a folder… it becomes part of your daily life.",
      },
      spouse: {
        label: "Needs to talk to spouse",
        clientCue: "I need to talk to my husband first.",
        response:
          "Of course—that’s such an important part of the decision. What I can do is send you a simple overview that makes it easy to share, and I’m always happy to answer any questions he might have as well. And if it helps, I can hold a date for you while you talk it over—no pressure at all.",
      },
      not_ready: {
        label: "Not ready",
        clientCue: "I’m not ready yet.",
        response:
          "That’s completely okay. Usually when someone feels that way, it’s not about timing—it’s about not feeling fully clear yet. Would it help if I showed you what this could look like for you specifically so you can decide from a place of clarity?",
      },
      time: {
        label: "Timing concern",
        clientCue: "We’re just so busy right now.",
        response:
          "I completely understand. That’s exactly why I guide the process so closely—it keeps this from becoming one more thing on your plate. If timing is the biggest concern, we can look at a date that gives you breathing room while still preserving this season before it passes.",
      },
    },
  },
  buying: {
    label: "Buying Signal",
    objective: "Confidently guide them to the next step.",
    triggers: {
      sounds_nice: {
        label: "This sounds really nice",
        clientCue: "This actually sounds really nice.",
        response:
          "I’m so glad it resonates with you. The next step would be a quick design conversation so we can start shaping this around you and your daughter. I do have a couple of beautiful dates available—would you like me to hold one while we plan?",
      },
      next_steps: {
        label: "What are the next steps?",
        clientCue: "What are the next steps from here?",
        response:
          "Perfect—that’s exactly where we want to be. We’ll start with a short consultation where I guide you through everything and begin designing your session. From there, we choose your date and start bringing it to life.",
      },
    },
  },
  disengagement: {
    label: "Disengagement Recovery",
    objective: "Recover clarity or exit gracefully without pressure.",
    triggers: {
      think_about_it: {
        label: "Needs to think about it",
        clientCue: "I think I need to think about it.",
        response:
          "That makes sense—and I want you to feel completely confident in whatever you decide. Usually when someone feels unsure, it’s because they’re missing a clear picture of what this would actually become. Would it help if I showed you a few examples of how this looks for other clients so you can really see the difference?",
      },
      pass: {
        label: "Going to pass",
        clientCue: "I think I’m going to pass for now.",
        response:
          "I completely understand—and I really appreciate you sharing that with me. If anything changes or you find yourself wanting something more intentional in the future, I’m always here to guide you through it.",
      },
    },
  },
};

const stageOrder = Object.keys(responseLibrary);

const callCoach = {
  discovery:
    "Slow down. Ask one emotionally open question. Do not explain too much yet.",
  desire:
    "Reflect what matters and expand the emotional why. Keep the client talking.",
  trust:
    "Normalize fear. Position yourself as the calm guide.",
  objection:
    "Do not repeat discovery language. Interrupt the pattern, explain what is different, and lead.",
  buying:
    "Be direct. Guide to date, consult, or reservation.",
  disengagement:
    "Restore clarity or release with grace. Never chase.",
};

const scenarioCases = [
  {
    name: "Mother-Daughter, Past Bad Experience",
    stage: "objection",
    trigger: "past_experience",
    clientMessage:
      "I’ve done family photos before and honestly they just sat on my phone. I don’t want to spend money and end up in the same place again.",
  },
  {
    name: "Interested but Overwhelmed",
    stage: "discovery",
    trigger: "overwhelmed",
    clientMessage:
      "I love your work, I’m just overwhelmed and not really sure where to start.",
  },
  {
    name: "Warm Lead Ready for Next Step",
    stage: "buying",
    trigger: "next_steps",
    clientMessage:
      "This sounds beautiful. What would the next step be?",
  },
  {
    name: "Spouse Barrier",
    stage: "objection",
    trigger: "spouse",
    clientMessage:
      "I really like this, but I need to talk to my husband before I commit to anything.",
  },
];

function getResponse(stage, trigger) {
  return responseLibrary?.[stage]?.triggers?.[trigger]?.response || "";
}

function getTriggersForStage(stage) {
  return Object.entries(responseLibrary[stage]?.triggers || {}).map(([key, value]) => ({
    key,
    ...value,
  }));
}

export default function TexasVogueLuApp() {
  const [stage, setStage] = useState("discovery");
  const [trigger, setTrigger] = useState("just_looking");
  const [clientInput, setClientInput] = useState(responseLibrary.discovery.triggers.just_looking.clientCue);
  const [generatedResponse, setGeneratedResponse] = useState(getResponse("discovery", "just_looking"));
  const [copied, setCopied] = useState(false);
  const [mode, setMode] = useState("text");
  const [selectedScenario, setSelectedScenario] = useState("Mother-Daughter, Past Bad Experience");
  const [conversationLog, setConversationLog] = useState([
    {
      speaker: "client",
      text: "Hi, I’ve been looking at your work and I’m interested in doing something with my daughter, but I’m honestly not totally sure what I’d want yet.",
    },
    {
      speaker: "assistant",
      text: "Absolutely—and honestly, that’s the perfect place to start. Most of my clients don’t come in with a clear plan… they just know they want something meaningful.",
    },
  ]);

  const triggerOptions = useMemo(() => getTriggersForStage(stage), [stage]);

  const selectedStageMeta = responseLibrary[stage];
  const selectedTriggerMeta = responseLibrary[stage].triggers[trigger];

  const applySelection = (nextStage, nextTrigger) => {
    const cue = responseLibrary[nextStage].triggers[nextTrigger].clientCue;
    const response = responseLibrary[nextStage].triggers[nextTrigger].response;
    setStage(nextStage);
    setTrigger(nextTrigger);
    setClientInput(cue);
    setGeneratedResponse(response);
  };

  const handleStageChange = (value) => {
    const firstTrigger = Object.keys(responseLibrary[value].triggers)[0];
    applySelection(value, firstTrigger);
  };

  const handleTriggerChange = (value) => {
    applySelection(stage, value);
  };

  const handleGenerate = () => {
    const response = getResponse(stage, trigger);
    setGeneratedResponse(response);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(generatedResponse);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  const loadScenario = (scenarioName) => {
    const found = scenarioCases.find((item) => item.name === scenarioName);
    if (!found) return;
    setSelectedScenario(scenarioName);
    applySelection(found.stage, found.trigger);
    setClientInput(found.clientMessage);
    setConversationLog([
      { speaker: "client", text: found.clientMessage },
      { speaker: "assistant", text: getResponse(found.stage, found.trigger) },
    ]);
  };

  const addToConversation = () => {
    if (!clientInput.trim()) return;
    setConversationLog((prev) => [
      ...prev,
      { speaker: "client", text: clientInput.trim() },
      { speaker: "assistant", text: generatedResponse.trim() },
    ]);
  };

  const resetConversation = () => {
    setConversationLog([]);
  };

  return (
    <div className="min-h-screen bg-stone-950 text-stone-100">
      <div className="mx-auto max-w-7xl px-4 py-8 md:px-8 lg:px-10">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <Badge className="rounded-full border border-amber-200/20 bg-amber-100/10 px-4 py-1 text-amber-100">
              Texas Vogue AI Concierge
            </Badge>
            <Badge variant="outline" className="rounded-full border-stone-700 text-stone-300">
              Luxury LU Conversion Engine
            </Badge>
          </div>
          <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">LU Response Studio</h1>
          <p className="mt-3 max-w-3xl text-base leading-7 text-stone-300 md:text-lg">
            A stage-aware, trigger-based backend tool for emotionally intelligent client replies, objection handling,
            and luxury sales guidance across text and discovery calls.
          </p>
        </motion.div>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="space-y-6">
            <Card className="rounded-3xl border-stone-800 bg-stone-900/80 shadow-2xl shadow-black/20">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between gap-4">
                  <CardTitle className="flex items-center gap-2 text-2xl">
                    <Brain className="h-5 w-5 text-amber-200" />
                    Response Generator
                  </CardTitle>
                  <div className="flex items-center gap-2 rounded-full border border-stone-800 bg-stone-950 p-1">
                    <Button
                      variant={mode === "text" ? "default" : "ghost"}
                      className="rounded-full"
                      onClick={() => setMode("text")}
                    >
                      <MessageSquare className="mr-2 h-4 w-4" /> Text
                    </Button>
                    <Button
                      variant={mode === "call" ? "default" : "ghost"}
                      className="rounded-full"
                      onClick={() => setMode("call")}
                    >
                      <Phone className="mr-2 h-4 w-4" /> Call
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm text-stone-400">Stage</label>
                    <Select value={stage} onValueChange={handleStageChange}>
                      <SelectTrigger className="h-12 rounded-2xl border-stone-800 bg-stone-950">
                        <SelectValue placeholder="Choose stage" />
                      </SelectTrigger>
                      <SelectContent>
                        {stageOrder.map((item) => (
                          <SelectItem key={item} value={item}>
                            {responseLibrary[item].label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm text-stone-400">Trigger</label>
                    <Select value={trigger} onValueChange={handleTriggerChange}>
                      <SelectTrigger className="h-12 rounded-2xl border-stone-800 bg-stone-950">
                        <SelectValue placeholder="Choose trigger" />
                      </SelectTrigger>
                      <SelectContent>
                        {triggerOptions.map((item) => (
                          <SelectItem key={item.key} value={item.key}>
                            {item.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <Card className="rounded-2xl border-stone-800 bg-stone-950/90">
                    <CardContent className="p-4">
                      <p className="mb-2 text-xs uppercase tracking-[0.22em] text-stone-500">Stage Objective</p>
                      <p className="text-sm leading-6 text-stone-200">{selectedStageMeta.objective}</p>
                    </CardContent>
                  </Card>
                  <Card className="rounded-2xl border-stone-800 bg-stone-950/90">
                    <CardContent className="p-4">
                      <p className="mb-2 text-xs uppercase tracking-[0.22em] text-stone-500">Call Coach</p>
                      <p className="text-sm leading-6 text-stone-200">{callCoach[stage]}</p>
                    </CardContent>
                  </Card>
                </div>

                <div className="space-y-2">
                  <label className="text-sm text-stone-400">Client Message / Cue</label>
                  <Textarea
                    value={clientInput}
                    onChange={(e) => setClientInput(e.target.value)}
                    className="min-h-[120px] rounded-2xl border-stone-800 bg-stone-950 text-stone-100"
                  />
                </div>

                <div className="flex flex-wrap gap-3">
                  <Button onClick={handleGenerate} className="rounded-full px-5">
                    <Sparkles className="mr-2 h-4 w-4" /> Generate Response
                  </Button>
                  <Button variant="outline" onClick={handleCopy} className="rounded-full border-stone-700 bg-transparent">
                    <Copy className="mr-2 h-4 w-4" /> {copied ? "Copied" : "Copy"}
                  </Button>
                  <Button variant="outline" onClick={addToConversation} className="rounded-full border-stone-700 bg-transparent">
                    <ChevronRight className="mr-2 h-4 w-4" /> Add to Test Panel
                  </Button>
                </div>

                <div className="rounded-3xl border border-amber-200/15 bg-gradient-to-br from-stone-950 to-stone-900 p-5">
                  <div className="mb-3 flex items-center justify-between gap-3">
                    <div>
                      <p className="text-xs uppercase tracking-[0.22em] text-amber-100/60">Generated Response</p>
                      <p className="mt-1 text-sm text-stone-400">{selectedTriggerMeta.label}</p>
                    </div>
                    <Badge className="rounded-full bg-amber-100/10 text-amber-100">{mode === "call" ? "Call-ready" : "Text-ready"}</Badge>
                  </div>
                  <p className="whitespace-pre-wrap text-[15px] leading-7 text-stone-100">{generatedResponse}</p>
                </div>
              </CardContent>
            </Card>

            <Tabs defaultValue="simulator" className="w-full">
              <TabsList className="grid w-full grid-cols-2 rounded-2xl bg-stone-900">
                <TabsTrigger value="simulator" className="rounded-2xl">Testing Panel</TabsTrigger>
                <TabsTrigger value="library" className="rounded-2xl">Full Library</TabsTrigger>
              </TabsList>

              <TabsContent value="simulator" className="mt-4">
                <Card className="rounded-3xl border-stone-800 bg-stone-900/80">
                  <CardHeader>
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <CardTitle className="text-2xl">Scenario Simulator</CardTitle>
                      <div className="flex gap-2">
                        <Select value={selectedScenario} onValueChange={loadScenario}>
                          <SelectTrigger className="w-[280px] rounded-2xl border-stone-800 bg-stone-950">
                            <SelectValue placeholder="Load scenario" />
                          </SelectTrigger>
                          <SelectContent>
                            {scenarioCases.map((scenario) => (
                              <SelectItem key={scenario.name} value={scenario.name}>
                                {scenario.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <Button variant="outline" onClick={resetConversation} className="rounded-full border-stone-700 bg-transparent">
                          <RefreshCcw className="mr-2 h-4 w-4" /> Clear
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <ScrollArea className="h-[360px] rounded-2xl border border-stone-800 bg-stone-950 p-4">
                      <div className="space-y-4">
                        {conversationLog.length === 0 ? (
                          <p className="text-sm text-stone-500">No messages yet. Load a scenario or add your current exchange.</p>
                        ) : (
                          conversationLog.map((entry, index) => (
                            <div
                              key={`${entry.speaker}-${index}`}
                              className={`max-w-[88%] rounded-3xl px-4 py-3 text-sm leading-6 ${
                                entry.speaker === "client"
                                  ? "mr-auto border border-stone-800 bg-stone-900 text-stone-200"
                                  : "ml-auto bg-amber-100/10 text-amber-50"
                              }`}
                            >
                              <p className="mb-1 text-[11px] uppercase tracking-[0.22em] opacity-70">
                                {entry.speaker === "client" ? "Client" : "Texas Vogue"}
                              </p>
                              <p>{entry.text}</p>
                            </div>
                          ))
                        )}
                      </div>
                    </ScrollArea>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="library" className="mt-4">
                <Card className="rounded-3xl border-stone-800 bg-stone-900/80">
                  <CardHeader>
                    <CardTitle className="text-2xl">Complete Response Library</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Accordion type="single" collapsible className="w-full">
                      {stageOrder.map((stageKey) => (
                        <AccordionItem key={stageKey} value={stageKey} className="border-stone-800">
                          <AccordionTrigger className="text-left text-base text-stone-100">
                            <div>
                              <div className="font-medium">{responseLibrary[stageKey].label}</div>
                              <div className="mt-1 text-sm font-normal text-stone-400">
                                {responseLibrary[stageKey].objective}
                              </div>
                            </div>
                          </AccordionTrigger>
                          <AccordionContent>
                            <div className="space-y-4">
                              {Object.entries(responseLibrary[stageKey].triggers).map(([triggerKey, item]) => (
                                <Card key={triggerKey} className="rounded-2xl border-stone-800 bg-stone-950/90">
                                  <CardContent className="p-4">
                                    <div className="mb-2 flex items-center justify-between gap-2">
                                      <h3 className="font-medium text-stone-100">{item.label}</h3>
                                      <Button
                                        size="sm"
                                        variant="outline"
                                        className="rounded-full border-stone-700 bg-transparent"
                                        onClick={() => applySelection(stageKey, triggerKey)}
                                      >
                                        Load
                                      </Button>
                                    </div>
                                    <p className="mb-3 text-sm text-stone-400">
                                      <span className="text-stone-500">Client cue:</span> {item.clientCue}
                                    </p>
                                    <p className="text-sm leading-7 text-stone-200">{item.response}</p>
                                  </CardContent>
                                </Card>
                              ))}
                            </div>
                          </AccordionContent>
                        </AccordionItem>
                      ))}
                    </Accordion>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          <div className="space-y-6">
            <Card className="rounded-3xl border-stone-800 bg-stone-900/80">
              <CardHeader>
                <CardTitle className="text-2xl">Luxury Sales Rules</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm leading-7 text-stone-300">
                <p>1. Do not repeat discovery language once the client moves into objection.</p>
                <p>2. When fear appears, address the fear directly before asking another question.</p>
                <p>3. Use pattern interruption: explain how most photographers handle it, then contrast your process.</p>
                <p>4. Move from photos to finished artwork, meaning, and daily life impact.</p>
                <p>5. When buying signals appear, lead clearly. Do not get vague.</p>
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-stone-800 bg-gradient-to-br from-amber-100/10 to-stone-900">
              <CardHeader>
                <CardTitle className="text-2xl">Strong Response Formula</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm leading-7 text-stone-200">
                <p><span className="text-amber-100">Acknowledge:</span> show the client you heard the real concern.</p>
                <p><span className="text-amber-100">Interrupt:</span> call out the broken industry pattern.</p>
                <p><span className="text-amber-100">Differentiate:</span> explain what Texas Vogue does differently.</p>
                <p><span className="text-amber-100">Visualize:</span> show the outcome in her home and life.</p>
                <p><span className="text-amber-100">Lead:</span> offer the next clear step.</p>
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-stone-800 bg-stone-900/80">
              <CardHeader>
                <CardTitle className="text-2xl">Phone Call Notes</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm leading-7 text-stone-300">
                <p>Use shorter sentences.</p>
                <p>Pause after emotional lines.</p>
                <p>Ask one question at a time.</p>
                <p>On calls, confidence matters more than polish.</p>
                <p>When she hesitates, do not back away—clarify and lead.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
