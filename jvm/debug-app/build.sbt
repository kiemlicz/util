lazy val root = (project in file("."))
  .settings(
    name := "debug-app",
    organization := "io.github.kiemlicz",
    description := "To debug things",
    licenses += "The MIT License" -> url("https://opensource.org/licenses/MIT"),
    scalacOptions ++= Seq(
      "-encoding", "utf8",
      "-deprecation",
      "-unchecked",
      "-Xlint",
    ),
    resolvers += "Sonatype releases".at("https://oss.sonatype.org/content/repositories/releases/"),
    libraryDependencies ++= Seq(
      "org.jgroups" % "jgroups" % "5.1.6.Final",
      "io.monix" %% "monix" % "3.4.0",
    ),
    dockerBaseImage := "openjdk:11.0-jdk-slim",
    discoveredMainClasses := Seq(
      "io.github.kiemlicz.CPUs#main"
    ),
    dockerEntrypoint := Seq(
      "/opt/docker/bin/stress"
    )
  )
  .enablePlugins(JavaServerAppPackaging, DockerPlugin)
